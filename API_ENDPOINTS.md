# PrintPro API - Complete Endpoints Reference

## 🔗 Base URL
```
http://localhost:8000/api
```

## 📍 All Available Endpoints

### 🔐 Authentication & User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register/` | Register new user | ❌ |
| POST | `/auth/login/` | Login and get JWT tokens | ❌ |
| POST | `/auth/token/refresh/` | Refresh access token | ❌ |
| GET | `/auth/profile/` | Get current user profile | ✅ |
| PUT | `/auth/profile/update/` | Update user profile | ✅ |
| PATCH | `/auth/profile/update/` | Partial update profile | ✅ |
| POST | `/auth/change-password/` | Change password | ✅ |

### 📂 Categories

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/categories/` | List all categories | ❌ |
| GET | `/categories/{slug}/` | Get category details | ❌ |
| GET | `/categories/{slug}/products/` | Get products in category | ❌ |
| POST | `/categories/` | Create category | ✅ Admin |
| PUT | `/categories/{slug}/` | Update category | ✅ Admin |
| PATCH | `/categories/{slug}/` | Partial update | ✅ Admin |
| DELETE | `/categories/{slug}/` | Delete category | ✅ Admin |

### 🛍️ Products

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/products/` | List all products (paginated) | ❌ |
| GET | `/products/{slug}/` | Get product details | ❌ |
| GET | `/products/featured/` | Get featured products | ❌ |
| GET | `/products/search/` | Advanced product search | ❌ |
| POST | `/products/` | Create product | ✅ Admin |
| PUT | `/products/{slug}/` | Update product | ✅ Admin |
| PATCH | `/products/{slug}/` | Partial update | ✅ Admin |
| DELETE | `/products/{slug}/` | Delete product | ✅ Admin |

#### Product Search Parameters
```
GET /products/search/?q=keyword&category=slug&min_price=100&max_price=500&in_stock=true
```

#### Product Filtering
```
GET /products/?category=1&is_featured=true&in_stock=true&search=stamp&ordering=-created_at
```

### 🛒 Shopping Cart

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/cart/retrieve/` | Get user's cart | ✅ |
| POST | `/cart/add_item/` | Add item to cart | ✅ |
| PUT | `/cart/items/{item_id}/` | Update cart item quantity | ✅ |
| PATCH | `/cart/items/{item_id}/` | Partial update cart item | ✅ |
| DELETE | `/cart/items/{item_id}/` | Remove item from cart | ✅ |
| POST | `/cart/clear/` | Clear entire cart | ✅ |

### 📦 Orders

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/orders/` | List user's orders | ✅ |
| GET | `/orders/{id}/` | Get order details | ✅ |
| POST | `/orders/` | Create custom order | ✅ |
| POST | `/orders/checkout/` | Create order from cart | ✅ |
| POST | `/orders/{id}/update_status/` | Update order status | ✅ Admin |
| POST | `/orders/{id}/update_payment_status/` | Update payment status | ✅ Admin |

#### Order Status Values
- `pending` - Order received
- `confirmed` - Order confirmed
- `processing` - Being processed
- `ready` - Ready for shipping
- `shipped` - Shipped
- `delivered` - Delivered
- `cancelled` - Cancelled

#### Payment Status Values
- `pending` - Payment pending
- `paid` - Payment received
- `failed` - Payment failed
- `refunded` - Payment refunded

### 🔧 Admin (Admin Only)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/admin/statistics/` | Get dashboard statistics | ✅ Admin |

### 📊 Product Management (Admin)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/product-images/` | List product images | ✅ Admin |
| POST | `/product-images/` | Add product image | ✅ Admin |
| GET | `/product-images/{id}/` | Get image details | ✅ Admin |
| PUT | `/product-images/{id}/` | Update image | ✅ Admin |
| DELETE | `/product-images/{id}/` | Delete image | ✅ Admin |
| GET | `/product-specifications/` | List specifications | ✅ Admin |
| POST | `/product-specifications/` | Add specification | ✅ Admin |
| PUT | `/product-specifications/{id}/` | Update specification | ✅ Admin |
| DELETE | `/product-specifications/{id}/` | Delete specification | ✅ Admin |
| GET | `/product-variants/` | List variants | ✅ Admin |
| POST | `/product-variants/` | Add variant | ✅ Admin |
| PUT | `/product-variants/{id}/` | Update variant | ✅ Admin |
| DELETE | `/product-variants/{id}/` | Delete variant | ✅ Admin |

### 📖 Documentation

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/schema/` | OpenAPI schema (JSON) | ❌ |
| GET | `/docs/` | Swagger UI | ❌ |
| GET | `/redoc/` | ReDoc documentation | ❌ |

---

## 📝 Request/Response Examples

### 1. Register User

**Request:**
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+971501234567"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "phone": "+971501234567"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully!"
}
```

### 2. Login

**Request:**
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Get Products

**Request:**
```http
GET /api/products/
```

**Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Shiny R-532D Professional Dater Stamp",
      "slug": "shiny-r-532d",
      "category": 1,
      "category_name": "Dater Stamp Products",
      "category_slug": "dater-stamp-products",
      "short_description": "Professional dater stamp with customizable text",
      "price": "150.00",
      "sale_price": null,
      "current_price": "150.00",
      "main_image": "/media/products/stamp1.jpg",
      "in_stock": true,
      "is_featured": true,
      "created_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### 4. Get Product Details

**Request:**
```http
GET /api/products/shiny-r-532d/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Shiny R-532D Professional Dater Stamp",
  "slug": "shiny-r-532d",
  "category": {
    "id": 1,
    "name": "Dater Stamp Products",
    "slug": "dater-stamp-products",
    "image": "/media/categories/stamps.jpg"
  },
  "description": "Professional dater stamp with date, company name and received text. Perfect for office use.",
  "short_description": "Professional dater stamp with customizable text",
  "price": "150.00",
  "sale_price": null,
  "current_price": "150.00",
  "stock_quantity": 50,
  "track_inventory": true,
  "in_stock": true,
  "sku": "SHINY-R532D",
  "weight": "0.20",
  "main_image": "/media/products/stamp1.jpg",
  "images": [
    {
      "id": 1,
      "image": "/media/products/stamp1-2.jpg",
      "alt_text": "Side view",
      "order": 1
    }
  ],
  "specifications": [
    {
      "id": 1,
      "key": "Size",
      "value": "42mm x 25mm",
      "order": 1
    },
    {
      "id": 2,
      "key": "Material",
      "value": "ABS Plastic",
      "order": 2
    }
  ],
  "variants": [],
  "is_active": true,
  "is_featured": true,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### 5. Add to Cart

**Request:**
```http
POST /api/cart/add_item/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

**Response (201 Created):**
```json
{
  "message": "Item added to cart successfully!",
  "cart": {
    "id": 1,
    "items": [
      {
        "id": 1,
        "product": 1,
        "product_name": "Shiny R-532D Professional Dater Stamp",
        "product_slug": "shiny-r-532d",
        "product_image": "/media/products/stamp1.jpg",
        "variant": null,
        "variant_name": null,
        "quantity": 2,
        "price": "150.00",
        "total_price": "300.00"
      }
    ],
    "total_items": 2,
    "subtotal": "300.00"
  }
}
```

### 6. Get Cart

**Request:**
```http
GET /api/cart/retrieve/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (200 OK):**
```json
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product": 1,
      "product_name": "Shiny R-532D Professional Dater Stamp",
      "product_slug": "shiny-r-532d",
      "product_image": "/media/products/stamp1.jpg",
      "quantity": 2,
      "price": "150.00",
      "total_price": "300.00"
    }
  ],
  "total_items": 2,
  "subtotal": "300.00"
}
```

### 7. Checkout (Create Order from Cart)

**Request:**
```http
POST /api/orders/checkout/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+971501234567",
  "company_name": "ABC Trading",
  "address_line_1": "123 Business Bay",
  "address_line_2": "Office 456",
  "city": "Dubai",
  "state": "Dubai",
  "country": "UAE",
  "postal_code": "12345",
  "order_notes": "Please deliver before 5 PM"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "order_number": "ORD-20250115-A1B2C3D4",
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+971501234567",
  "company_name": "ABC Trading",
  "full_address": "123 Business Bay, Office 456, Dubai, Dubai, UAE, 12345",
  "order_notes": "Please deliver before 5 PM",
  "subtotal": "300.00",
  "shipping_cost": "0.00",
  "tax": "0.00",
  "total": "300.00",
  "status": "pending",
  "payment_status": "pending",
  "items": [
    {
      "id": 1,
      "product": 1,
      "product_name": "Shiny R-532D Professional Dater Stamp",
      "product_slug": "shiny-r-532d",
      "product_image": "/media/products/stamp1.jpg",
      "quantity": 2,
      "price": "150.00",
      "total": "300.00"
    }
  ],
  "files": [],
  "created_at": "2025-01-15T11:00:00Z"
}
```

### 8. Get Orders

**Request:**
```http
GET /api/orders/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "order_number": "ORD-20250115-A1B2C3D4",
      "full_name": "John Doe",
      "email": "john@example.com",
      "phone": "+971501234567",
      "status": "pending",
      "payment_status": "pending",
      "total": "300.00",
      "items_count": 1,
      "created_at": "2025-01-15T11:00:00Z",
      "updated_at": "2025-01-15T11:00:00Z"
    }
  ]
}
```

### 9. Search Products

**Request:**
```http
GET /api/products/search/?q=stamp&category=dater-stamp-products&in_stock=true&min_price=100&max_price=200
```

**Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Shiny R-532D Professional Dater Stamp",
      "slug": "shiny-r-532d",
      "category_name": "Dater Stamp Products",
      "price": "150.00",
      "current_price": "150.00",
      "in_stock": true
    }
  ]
}
```

### 10. Admin Statistics

**Request:**
```http
GET /api/admin/statistics/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc... (admin token)
```

**Response (200 OK):**
```json
{
  "orders": {
    "total": 125,
    "pending": 15,
    "completed": 95
  },
  "revenue": {
    "total": 45250.50,
    "last_30_days": 12340.00
  },
  "products": {
    "total": 48,
    "out_of_stock": 3
  },
  "users": {
    "total": 234,
    "new_last_30_days": 28
  },
  "recent_orders": [...]
}
```

---

## 🔑 Authentication Header Format

For all authenticated endpoints:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Server Error
```json
{
  "error": "Internal server error"
}
```

---

## 🎯 Quick Test Commands

```bash
# Get all products
curl http://localhost:8000/api/products/

# Get categories
curl http://localhost:8000/api/categories/

# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"Test123","password_confirm":"Test123","first_name":"Test","last_name":"User"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123"}'

# Get profile (with token)
curl http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

**Total Endpoints: 30+**
**Interactive Docs: http://localhost:8000/api/docs/**

