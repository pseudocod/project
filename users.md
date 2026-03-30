# Users Routes Documentation

## Description
Group: User management endpoints
Provides endpoints to retrieve and update the authenticated user's profile and address, and to list/retrieve users.

---

## GET /users/me

### Title
Get My Profile

### Method
GET

### Path
`/users/me`

### Summary
Returns the full profile of the currently authenticated user.

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

---

### Request Body
None

---

### Responses

#### 200 OK
Schema: See `src/models/user.py → UserResponseDTO`

Example:

```json
{
  "id": 3,
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "phone": "+40712345678",
  "role": "customer",
  "is_active": true,
  "created_at": "2026-01-10T09:00:00Z",
  "updated_at": null
}
```

#### 401 Unauthorized
```json
{ "detail": "Missing or invalid Authorization header" }
```

---

### Example cURL

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer <token>"
```

---

## PATCH /users/me

### Title
Update My Profile

### Method
PATCH

### Path
`/users/me`

### Summary
Partially updates the authenticated user's profile. Only fields included in the request body are updated. If the new email is already in use by another account, a 409 is returned — the check happens before the DB write.

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

Schema: See `src/models/user.py → UserUpdateDTO`

All fields are optional — send only what you want to change.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `first_name` | string | No | Updated first name. |
| `last_name` | string | No | Updated last name. |
| `phone` | string | No | Updated phone number. |
| `email` | string (email) | No | Updated email address. Must be unique. |

Example:

```json
{
  "first_name": "Alicia",
  "email": "alicia@example.com"
}
```

---

### Responses

#### 200 OK
Returns the updated user profile.

```json
{
  "id": 3,
  "email": "alicia@example.com",
  "first_name": "Alicia",
  "last_name": "Smith",
  "phone": "+40712345678",
  "role": "customer",
  "is_active": true,
  "created_at": "2026-01-10T09:00:00Z",
  "updated_at": "2026-03-30T11:00:00Z"
}
```

#### 401 Unauthorized
```json
{ "detail": "Missing or invalid Authorization header" }
```

#### 409 Conflict
The new email is already registered to another account.

```json
{ "detail": "Email 'alicia@example.com' is already in use." }
```

#### 422 Unprocessable Entity
Invalid email format.

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address"
    }
  ]
}
```

---

### Notes
- Email uniqueness is checked with an explicit query before the commit, not inferred from a DB error.
- Sending the same email the user already has is valid and produces no conflict.

### Example cURL

```bash
curl -X PATCH "http://localhost:8000/users/me" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{ "first_name": "Alicia" }'
```

---

## PUT /users/me/address

### Title
Create or Update My Address

### Method
PUT

### Path
`/users/me/address`

### Summary
Creates the user's address if one doesn't exist yet, or fully replaces it if one does. All fields are always required — this is a full replacement, not a partial update. The client does not need to know whether an address already exists.

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

Schema: See `src/models/user.py → AddressDTO`

All fields are required.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `street` | string | Yes | Street name and number. |
| `city` | string | Yes | City. |
| `state` | string | Yes | State or county. |
| `postal_code` | string | Yes | Postal / ZIP code. |
| `country` | string | Yes | Country. |

Example:

```json
{
  "street": "123 Main St",
  "city": "Bucharest",
  "state": "Ilfov",
  "postal_code": "010101",
  "country": "Romania"
}
```

---

### Responses

#### 200 OK
Returns the address as saved.

```json
{
  "street": "123 Main St",
  "city": "Bucharest",
  "state": "Ilfov",
  "postal_code": "010101",
  "country": "Romania"
}
```

#### 401 Unauthorized
```json
{ "detail": "Missing or invalid Authorization header" }
```

#### 422 Unprocessable Entity
A required field is missing.

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "postal_code"],
      "msg": "Field required"
    }
  ]
}
```

---

### Notes
- Idempotent — calling PUT with the same data multiple times always produces the same result.
- Internally uses `flush()` + single `commit()` when creating, so address creation and linking to the user are atomic.

### Example cURL

```bash
curl -X PUT "http://localhost:8000/users/me/address" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "street": "123 Main St",
    "city": "Bucharest",
    "state": "Ilfov",
    "postal_code": "010101",
    "country": "Romania"
  }'
```

---

## GET /users

### Title
List Users (Paginated)

### Method
GET

### Path
`/users/`

### Summary
Returns a paginated list of all users. Optionally filter by email substring.

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
| `search` | string | No | — | Filter by email (case-insensitive substring). |

### Request Headers
`Authorization: Bearer <token>`

---

### Request Body
None

---

### Responses

#### 200 OK
Schema: See `src/models/user.py → PaginatedUsersResponse`

```json
{
  "total_items": 21,
  "page": 1,
  "items": [
    {
      "id": 1,
      "email": "admin@example.com",
      "first_name": "Admin",
      "last_name": "User",
      "phone": null,
      "role": "admin",
      "is_active": true,
      "created_at": "2026-01-01T00:00:00Z",
      "updated_at": null
    }
  ]
}
```

#### 401 Unauthorized
```json
{ "detail": "Missing or invalid Authorization header" }
```

---

### Example cURL

```bash
curl -X GET "http://localhost:8000/users/?page=1&limit=10&search=alice" \
  -H "Authorization: Bearer <token>"
```

---

## GET /users/{user_id}

### Title
Get User by ID

### Method
GET

### Path
`/users/{user_id}`

### Summary
Returns the profile of a specific user by ID.

### Authentication
Required — Bearer JWT token

### Permissions
Authenticated users only

---

### Path Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `user_id` | integer | Yes | ID of the user to retrieve. |

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
```json
{
  "id": 3,
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "phone": "+40712345678",
  "role": "customer",
  "is_active": true,
  "created_at": "2026-01-10T09:00:00Z",
  "updated_at": null
}
```

#### 401 Unauthorized
```json
{ "detail": "Missing or invalid Authorization header" }
```

#### 404 Not Found
```json
{ "detail": "User with ID 999 not found" }
```

#### 422 Unprocessable Entity
`user_id` is not a valid integer.

---

### Example cURL

```bash
curl -X GET "http://localhost:8000/users/3" \
  -H "Authorization: Bearer <token>"
```

---

## Related Endpoints
- GET `/users/me`
- PATCH `/users/me`
- PUT `/users/me/address`
- GET `/users/`
- GET `/users/{user_id}`