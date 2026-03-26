# Orders Routes Documentation

## Description
Group: Order management endpoints
Provides endpoints to place orders. Handles stock reservation, order creation, and order item snapshots within a single atomic transaction.

---

## POST /orders

### Title
Place Order

### Method
POST

### Path
`/orders`

### Summary
Creates a new order from a list of items. Validates stock availability, deducts stock atomically, snapshots product name and price at the time of purchase, and persists the order with status `pending`.

### Authentication
Required — Bearer JWT token

### Permissions
Authenticated users only

---

### Path Parameters
None

---

### Query Parameters
None

---

### Request Headers
`Authorization: Bearer <token>`
`Content-Type: application/json`

---

### Request Body

Schema: See `src/models/order.py → OrderRequestDTO`

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `items` | array | Yes | List of products to order. Must contain at least one item. No duplicate `product_id` values allowed. |
| `items[].product_id` | integer | Yes | ID of the product (must be > 0). |
| `items[].quantity` | integer | Yes | Quantity to order (must be > 0). |
| `payment_type` | string | Yes | Payment method. Accepted values: `"cash"`, `"card"`. |
| `shipping_address_id` | integer | Yes | ID of the shipping address (must be > 0). |
| `billing_address_id` | integer | Yes | ID of the billing address (must be > 0). |

Example:

```json
{
  "items": [
    { "product_id": 1, "quantity": 2 },
    { "product_id": 3, "quantity": 1 }
  ],
  "payment_type": "card",
  "shipping_address_id": 4,
  "billing_address_id": 4
}
```

---

### Responses

#### 201 Created
Order was successfully created.

Schema: See `src/models/order.py → OrderResponseDTO`

Example:

```json
{
  "id": 12,
  "status": "pending",
  "payment_type": "card",
  "shipping_address_id": 4,
  "billing_address_id": 4,
  "items": [
    {
      "product_id": 1,
      "name": "UltraBook Pro 14",
      "quantity": 2,
      "price_per_piece": 3499.99
    },
    {
      "product_id": 3,
      "name": "Wireless Mouse",
      "quantity": 1,
      "price_per_piece": 49.99
    }
  ]
}
```

#### 401 Unauthorized
When the Authorization header is missing or the token is invalid/expired.

```json
{
  "detail": "Missing or invalid Authorization header",
  "code": "MISSING_TOKEN"
}
```

#### 404 Not Found
When a product ID in the order does not exist.

```json
{
  "detail": "Product with ID 99 not found."
}
```

#### 409 Conflict
When a product is inactive or has insufficient stock.

```json
{
  "detail": "Product with ID 1 is not available."
}
```

```json
{
  "detail": "Insufficient stock for product 1: requested 5, available 2."
}
```

#### 422 Unprocessable Entity
When the request body fails validation (e.g., negative quantity, duplicate product IDs, invalid payment type).

```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "items", 0, "quantity"],
      "msg": "Input should be greater than 0",
      "input": -1
    }
  ]
}
```

---

### Order Notes
- Stock is deducted atomically using `SELECT FOR UPDATE` to prevent overselling under concurrent requests.
- Product `name` and `price_per_piece` are snapshotted at the time of purchase — future product changes do not affect existing orders.
- All orders are created with status `pending`.

### Example cURL — Place Order

```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      { "product_id": 1, "quantity": 2 }
    ],
    "payment_type": "card",
    "shipping_address_id": 4,
    "billing_address_id": 4
  }'
```

### Related Endpoints
- POST `/orders`