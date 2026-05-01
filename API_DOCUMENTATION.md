# E-Commerce API Documentation

Complete API reference for the E-Commerce platform.

## Base URL

```
http://localhost:5000/api
```

## Authentication

Most endpoints require authentication using JWT tokens.

### Headers

```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Login

Authenticate user and receive JWT token.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Get Current User

Get authenticated user information.

**Endpoint:** `GET /auth/me`

**Headers:** Requires authentication

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "phone": "+1234567890",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "country": "USA"
  }
}
```

---

## Product Endpoints

### Get All Products

Retrieve products with pagination and filters.

**Endpoint:** `GET /products`

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 12)
- `category_id` (int): Filter by category
- `search` (string): Search by product name
- `min_price` (float): Minimum price filter
- `max_price` (float): Maximum price filter
- `sort_by` (string): Sort field (price, name, created_at)
- `order` (string): Sort order (asc, desc)

**Example:**
```
GET /products?page=1&per_page=12&category_id=1&sort_by=price&order=asc
```

**Response:** `200 OK`
```json
{
  "products": [
    {
      "id": 1,
      "name": "Product Name",
      "description": "Product description",
      "price": 29.99,
      "category_id": 1,
      "category_name": "Electronics",
      "stock": 50,
      "image_url": "https://...",
      "is_active": true,
      "sku": "PROD-001",
      "average_rating": 4.5,
      "review_count": 10
    }
  ],
  "total": 100,
  "pages": 9,
  "current_page": 1,
  "per_page": 12
}
```

### Get Single Product

**Endpoint:** `GET /products/:id`

**Response:** `200 OK`
```json
{
  "product": {
    "id": 1,
    "name": "Product Name",
    "description": "Detailed product description",
    "price": 29.99,
    "category_id": 1,
    "category_name": "Electronics",
    "stock": 50,
    "image_url": "https://...",
    "is_active": true,
    "sku": "PROD-001",
    "average_rating": 4.5,
    "review_count": 10,
    "reviews": [
      {
        "id": 1,
        "user_name": "John Doe",
        "rating": 5,
        "comment": "Great product!",
        "created_at": "2024-01-01T00:00:00"
      }
    ]
  }
}
```

### Create Product (Admin Only)

**Endpoint:** `POST /products`

**Headers:** Requires admin authentication

**Request Body:**
```json
{
  "name": "New Product",
  "description": "Product description",
  "price": 29.99,
  "category_id": 1,
  "stock": 100,
  "sku": "PROD-001",
  "image": "base64_encoded_image_or_url"
}
```

**Response:** `201 Created`

### Update Product (Admin Only)

**Endpoint:** `PUT /products/:id`

**Headers:** Requires admin authentication

**Request Body:** Same as create (all fields optional)

**Response:** `200 OK`

### Delete Product (Admin Only)

**Endpoint:** `DELETE /products/:id`

**Headers:** Requires admin authentication

**Response:** `200 OK`

---

## Category Endpoints

### Get All Categories

**Endpoint:** `GET /categories`

**Response:** `200 OK`
```json
{
  "categories": [
    {
      "id": 1,
      "name": "Electronics",
      "description": "Electronic devices",
      "product_count": 25
    }
  ]
}
```

### Create Category (Admin Only)

**Endpoint:** `POST /categories`

**Request Body:**
```json
{
  "name": "New Category",
  "description": "Category description"
}
```

---

## Cart Endpoints

### Get Cart

**Endpoint:** `GET /cart`

**Headers:** Requires authentication

**Response:** `200 OK`
```json
{
  "cart_items": [
    {
      "id": 1,
      "product_id": 1,
      "product": {
        "id": 1,
        "name": "Product Name",
        "price": 29.99,
        "image_url": "https://..."
      },
      "quantity": 2,
      "subtotal": 59.98
    }
  ],
  "total": 59.98,
  "item_count": 1
}
```

### Add to Cart

**Endpoint:** `POST /cart`

**Headers:** Requires authentication

**Request Body:**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Response:** `201 Created`

### Update Cart Item

**Endpoint:** `PUT /cart/:id`

**Headers:** Requires authentication

**Request Body:**
```json
{
  "quantity": 3
}
```

**Response:** `200 OK`

### Remove from Cart

**Endpoint:** `DELETE /cart/:id`

**Headers:** Requires authentication

**Response:** `200 OK`

### Clear Cart

**Endpoint:** `DELETE /cart/clear`

**Headers:** Requires authentication

**Response:** `200 OK`

---

## Order Endpoints

### Get Orders

**Endpoint:** `GET /orders`

**Headers:** Requires authentication

**Query Parameters:**
- `page` (int): Page number
- `per_page` (int): Items per page
- `status` (string): Filter by status

**Response:** `200 OK`
```json
{
  "orders": [
    {
      "id": 1,
      "user_id": 1,
      "total_amount": 59.98,
      "status": "pending",
      "payment_status": "paid",
      "shipping_address": "123 Main St",
      "created_at": "2024-01-01T00:00:00",
      "items": [
        {
          "product_name": "Product Name",
          "quantity": 2,
          "price": 29.99,
          "subtotal": 59.98
        }
      ]
    }
  ],
  "total": 10,
  "pages": 1,
  "current_page": 1
}
```

### Create Order

**Endpoint:** `POST /orders`

**Headers:** Requires authentication

**Request Body:**
```json
{
  "shipping_address": "123 Main St",
  "shipping_city": "New York",
  "shipping_state": "NY",
  "shipping_zip": "10001",
  "shipping_country": "USA",
  "shipping_phone": "+1234567890",
  "payment_method": "stripe",
  "payment_intent_id": "pi_xxx",
  "notes": "Optional notes"
}
```

**Response:** `201 Created`

### Update Order Status (Admin Only)

**Endpoint:** `PUT /orders/:id/status`

**Headers:** Requires admin authentication

**Request Body:**
```json
{
  "status": "shipped",
  "payment_status": "paid",
  "notes": "Order shipped via FedEx"
}
```

**Valid Status Values:**
- `pending`
- `processing`
- `shipped`
- `delivered`
- `cancelled`

**Response:** `200 OK`

---

## Wishlist Endpoints

### Get Wishlist

**Endpoint:** `GET /wishlist`

**Headers:** Requires authentication

**Response:** `200 OK`

### Add to Wishlist

**Endpoint:** `POST /wishlist`

**Headers:** Requires authentication

**Request Body:**
```json
{
  "product_id": 1
}
```

**Response:** `201 Created`

### Remove from Wishlist

**Endpoint:** `DELETE /wishlist/:id`

**Headers:** Requires authentication

**Response:** `200 OK`

---

## Review Endpoints

### Get Product Reviews

**Endpoint:** `GET /reviews/product/:product_id`

**Response:** `200 OK`

### Create Review

**Endpoint:** `POST /reviews/product/:product_id`

**Headers:** Requires authentication

**Request Body:**
```json
{
  "rating": 5,
  "comment": "Great product!"
}
```

**Response:** `201 Created`

---

## Admin Endpoints

### Get Analytics

**Endpoint:** `GET /admin/analytics`

**Headers:** Requires admin authentication

**Response:** `200 OK`
```json
{
  "total_users": 100,
  "total_products": 50,
  "total_orders": 200,
  "total_sales": 5000.00,
  "recent_orders": 25,
  "recent_sales": 1000.00,
  "top_products": [],
  "low_stock_products": []
}
```

### Get Sales Data

**Endpoint:** `GET /admin/sales`

**Headers:** Requires admin authentication

**Query Parameters:**
- `period` (string): day, week, month, year

**Response:** `200 OK`

### Get All Users

**Endpoint:** `GET /admin/users`

**Headers:** Requires admin authentication

**Response:** `200 OK`

---

## Error Responses

All endpoints may return these error responses:

### 400 Bad Request
```json
{
  "error": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "Admin access required"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Server error message",
  "message": "Detailed error information"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. In production, consider adding rate limiting to prevent abuse.

## Pagination

List endpoints support pagination with these parameters:
- `page`: Page number (starts at 1)
- `per_page`: Items per page (default varies by endpoint)

Response includes:
- `total`: Total number of items
- `pages`: Total number of pages
- `current_page`: Current page number
- `per_page`: Items per page

---

## Testing with cURL

### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","first_name":"Test","last_name":"User"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### Get Products
```bash
curl http://localhost:5000/api/products
```

### Get Cart (with auth)
```bash
curl http://localhost:5000/api/cart \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

For more examples and testing, import the API collection into Postman or use the provided frontend application.
