# Orders Routes Documentation

## Description
Group: Order management endpoints
Provides endpoints to place orders, view order history, view a single order, and cancel orders.
Handles stock reservation, order creation, and order item snapshots within a single atomic transaction.

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

### Query Parameters
None

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
  "created_at": "2026-03-30T10:00:00Z",
  "items": [
    {
      "product_id": 1,
      "name": "UltraBook Pro 14",
      "quantity": 2,
      "price_per_piece": 3499.99
    },
    {
      "product_id": 3,
      "name": "Classic Cotton T-Shirt",
      "quantity": 1,
      "price_per_piece": 49.99
    }
  ]
}
```

#### 401 Unauthorized
Missing or invalid token.

```json
{ "detail": "Missing or invalid Authorization header" }
```

#### 404 Not Found
A product ID in the order does not exist.

```json
{ "detail": "Product with ID 99 not found." }
```

#### 409 Conflict
Product is inactive or has insufficient stock.

```json
{ "detail": "Product with ID 1 is not available." }
```

```json
{ "detail": "Insufficient stock for product 1: requested 5, available 2." }
```

#### 422 Unprocessable Entity
Request body fails validation (e.g., negative quantity, duplicate product IDs, invalid payment type).

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

### Example cURL

```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{ "product_id": 1, "quantity": 2 }],
    "payment_type": "card",
    "shipping_address_id": 4,
    "billing_address_id": 4
  }'
```

---

## GET /orders/me

### Title
Get My Order History

### Method
GET

### Path
`/orders/me`

### Summary
Returns a paginated list of all orders belonging to the currently authenticated user, sorted by most recent first. Each item is a summary with computed totals — no item-level detail is included.

### Authentication
Required — Bearer JWT token

### Permissions
Authenticated users only

---

### Path Parameters
None

### Query Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `page` | integer | No | `1` | Page number (≥ 1). |
| `limit` | integer | No | `10` | Items per page (1–100). |

### Request Headers
`Authorization: Bearer <token>`

---

### Request Body
None

---

### Responses

#### 200 OK
Schema: See `src/models/order.py → PaginatedOrdersResponse`

Example:

```json
{
  "total_items": 3,
  "page": 1,
  "items": [
    {
      "id": 12,
      "status": "pending",
      "payment_type": "card",
      "created_at": "2026-03-30T10:00:00Z",
      "total_amount": 6999.98,
      "item_count": 2
    },
    {
      "id": 7,
      "status": "delivered",
      "payment_type": "cash",
      "created_at": "2026-03-01T08:30:00Z",
      "total_amount": 49.99,
      "item_count": 1
    }
  ]
}
```

#### 401 Unauthorized
Missing or invalid token.

```json
{ "detail": "Missing or invalid Authorization header" }
```

---

### Notes
- `total_amount` is the sum of `price_per_piece × quantity` across all items in the order, computed from the snapshotted values at order time.
- `item_count` is the number of distinct order items (not total units).
- Results are ordered by `created_at` descending.

### Example cURL

```bash
curl -X GET "http://localhost:8000/orders/me?page=1&limit=10" \
  -H "Authorization: Bearer <token>"
```

---

## GET /orders/me/{order_id}

### Title
Get My Order by ID

### Method
GET

### Path
`/orders/me/{order_id}`

### Summary
Returns the full detail of a single order, including all items, addresses, and status. The order must belong to the authenticated user.

### Authentication
Required — Bearer JWT token

### Permissions
Authenticated users only

---

### Path Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | integer | Yes | ID of the order to retrieve. |

### Query Parameters
None

### Request Headers
`Authorization: Bearer <token>`

---

### Request Body
None

---

### Responses

#### 200 OK
Schema: See `src/models/order.py → OrderResponseDTO`

Example:

```json
{
  "id": 12,
  "status": "pending",
  "payment_type": "card",
  "shipping_address_id": 4,
  "billing_address_id": 4,
  "created_at": "2026-03-30T10:00:00Z",
  "items": [
    {
      "product_id": 1,
      "name": "UltraBook Pro 14",
      "quantity": 2,
      "price_per_piece": 3499.99
    }
  ]
}
```

#### 401 Unauthorized
Missing or invalid token.

```json
{ "detail": "Missing or invalid Authorization header" }
```

#### 403 Forbidden
The order exists but belongs to a different user.

```json
{ "detail": "Order with ID 12 does not belong to you." }
```

#### 404 Not Found
No order with that ID exists.

```json
{ "detail": "Order with ID 12 not found." }
```

---

### Example cURL

```bash
curl -X GET "http://localhost:8000/orders/me/12" \
  -H "Authorization: Bearer <token>"
```

---

## PATCH /orders/me/{order_id}/cancel

### Title
Cancel My Order

### Method
PATCH

### Path
`/orders/me/{order_id}/cancel`

### Summary
Cancels an order belonging to the authenticated user. Only orders in `pending` or `confirmed` status can be cancelled — orders that are already in delivery, delivered, completed, cancelled, or returned will be rejected.

### Authentication
Required — Bearer JWT token

### Permissions
Authenticated users only

---

### Path Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | integer | Yes | ID of the order to cancel. |

### Query Parameters
None

### Request Headers
`Authorization: Bearer <token>`

---

### Request Body
None

---

### Responses

#### 200 OK
Order was successfully cancelled. Returns the updated order.

Schema: See `src/models/order.py → OrderResponseDTO`

Example:

```json
{
  "id": 12,
  "status": "cancelled",
  "payment_type": "card",
  "shipping_address_id": 4,
  "billing_address_id": 4,
  "created_at": "2026-03-30T10:00:00Z",
  "items": [
    {
      "product_id": 1,
      "name": "UltraBook Pro 14",
      "quantity": 2,
      "price_per_piece": 3499.99
    }
  ]
}
```

#### 401 Unauthorized
Missing or invalid token.

```json
{ "detail": "Missing or invalid Authorization header" }
```

#### 403 Forbidden
The order exists but belongs to a different user.

```json
{ "detail": "Order with ID 12 does not belong to you." }
```

#### 404 Not Found
No order with that ID exists.

```json
{ "detail": "Order with ID 12 not found." }
```

#### 409 Conflict
The order is in a status that cannot be cancelled.

```json
{ "detail": "Order with ID 12 cannot be cancelled because its current status is 'in_delivery'." }
```

---

### Cancellable Statuses

| Status | Can Cancel? |
| :--- | :--- |
| `pending` | Yes |
| `confirmed` | Yes |
| `in_delivery` | No |
| `delivered` | No |
| `completed` | No |
| `cancelled` | No |
| `returned` | No |

### Example cURL

```bash
curl -X PATCH "http://localhost:8000/orders/me/12/cancel" \
  -H "Authorization: Bearer <token>"
```

---

## Related Endpoints
- POST `/orders/`
- GET `/orders/me`
- GET `/orders/me/{order_id}`
- PATCH `/orders/me/{order_id}/cancel`