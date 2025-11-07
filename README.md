# PrintPro API - Professional Printing Services Backend

A comprehensive Django REST Framework API for managing a printing business including products, categories, user accounts, shopping cart, and order management.

## 🚀 Features

### Core Features
- **User Authentication & Authorization** - JWT-based authentication with secure user management
- **Product Management** - Complete CRUD for products with images, specifications, and variants
- **Category Management** - Hierarchical categories for organizing products
- **Shopping Cart** - Full-featured cart system with session support
- **Order Management** - Complete order lifecycle with status tracking
- **File Uploads** - Support for design files, images, and documents
- **Admin Dashboard** - Rich admin interface with statistics and bulk operations
- **API Documentation** - Auto-generated OpenAPI/Swagger documentation

### Technical Features
- RESTful API design
- JWT authentication
- File upload support
- Advanced filtering and search
- Pagination
- CORS support for frontend integration
- Comprehensive admin interface
- Detailed error handling
- Production-ready

## 📋 Requirements

- Python 3.11+
- Django 5.2.8
- PostgreSQL (recommended for production) or SQLite (development)

## 🛠️ Installation

### 1. Clone and Setup Virtual Environment

```bash
cd printing-api
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root (optional for production):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL for production)
DATABASE_URL=postgresql://user:password@localhost:5432/printpro_db

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 4. Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Admin Interface

Access the Django admin interface at: http://localhost:8000/admin/

Use the superuser credentials you created during setup.

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Register New User

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

### Login

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using the Token

Include the access token in the Authorization header:

```http
GET /api/auth/profile/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 📍 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get current user profile
- `PUT /api/auth/profile/update/` - Update user profile
- `POST /api/auth/change-password/` - Change password

### Categories
- `GET /api/categories/` - List all categories
- `GET /api/categories/{slug}/` - Get category details
- `GET /api/categories/{slug}/products/` - Get products in category
- `POST /api/categories/` - Create category (admin)
- `PUT /api/categories/{slug}/` - Update category (admin)
- `DELETE /api/categories/{slug}/` - Delete category (admin)

### Products
- `GET /api/products/` - List all products (with filtering)
- `GET /api/products/{slug}/` - Get product details
- `GET /api/products/featured/` - Get featured products
- `GET /api/products/search/?q=keyword` - Search products
- `POST /api/products/` - Create product (admin)
- `PUT /api/products/{slug}/` - Update product (admin)
- `DELETE /api/products/{slug}/` - Delete product (admin)

### Cart (Authentication Required)
- `GET /api/cart/retrieve/` - Get current user's cart
- `POST /api/cart/add_item/` - Add item to cart
- `PUT /api/cart/items/{item_id}/` - Update cart item quantity
- `DELETE /api/cart/items/{item_id}/` - Remove item from cart
- `POST /api/cart/clear/` - Clear entire cart

### Orders (Authentication Required)
- `GET /api/orders/` - List user's orders
- `GET /api/orders/{id}/` - Get order details
- `POST /api/orders/` - Create new order
- `POST /api/orders/checkout/` - Create order from cart
- `POST /api/orders/{id}/update_status/` - Update order status (admin)
- `POST /api/orders/{id}/update_payment_status/` - Update payment status (admin)

### Admin
- `GET /api/admin/statistics/` - Get dashboard statistics (admin)

## 💡 Usage Examples

### Get All Products

```bash
curl -X GET http://localhost:8000/api/products/
```

### Add Item to Cart

```bash
curl -X POST http://localhost:8000/api/cart/add_item/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

### Create Order from Cart

```bash
curl -X POST http://localhost:8000/api/orders/checkout/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+971501234567",
    "address_line_1": "123 Main St",
    "city": "Dubai",
    "country": "UAE",
    "order_notes": "Please deliver before 5 PM"
  }'
```

### Search Products

```bash
curl -X GET "http://localhost:8000/api/products/search/?q=stamp&category=dater-stamp-products&in_stock=true"
```

## 🎨 Frontend Integration

### Next.js Example

```typescript
// lib/api.ts
const API_BASE_URL = 'http://localhost:8000/api';

export async function getProducts() {
  const response = await fetch(`${API_BASE_URL}/products/`);
  return response.json();
}

export async function addToCart(productId: number, quantity: number, token: string) {
  const response = await fetch(`${API_BASE_URL}/cart/add_item/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ product_id: productId, quantity })
  });
  return response.json();
}

export async function checkout(orderData: any, token: string) {
  const response = await fetch(`${API_BASE_URL}/orders/checkout/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(orderData)
  });
  return response.json();
}
```

## 🔧 Configuration

### Allowed Hosts (Production)

Update `config/settings.py`:

```python
ALLOWED_HOSTS = ['your-domain.com', 'api.your-domain.com']
```

### CORS Origins (Production)

Update `config/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
    "https://www.your-frontend-domain.com",
]
```

### Database (Production)

For PostgreSQL, update `DATABASES` in `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'printpro_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📦 Data Models

### User
- Extended Django user with phone, address, company details
- JWT authentication support

### Category
- Hierarchical categories
- Image support
- Active/inactive status

### Product
- Name, description, images
- Pricing with sale support
- Stock management
- Multiple images, specifications, variants
- SEO fields

### Cart & CartItem
- Per-user shopping carts
- Support for product variants
- Automatic price tracking

### Order & OrderItem
- Complete order information
- Status tracking (pending → confirmed → processing → shipped → delivered)
- Payment status tracking
- File attachments support
- Order history

## 🚀 Deployment

### Collect Static Files

```bash
python manage.py collectstatic
```

### Production Checklist

1. Set `DEBUG = False`
2. Configure proper `SECRET_KEY`
3. Set up PostgreSQL database
4. Configure static/media file serving (nginx/Apache)
5. Set up HTTPS
6. Configure email backend
7. Set up proper CORS origins
8. Enable database backups
9. Set up monitoring and logging

## 🤝 Contributing

This is a client project. For any issues or improvements, please contact the development team.

## 📄 License

Proprietary - All rights reserved.

## 📞 Support

For support and questions, please contact the development team.

---

**Built with ❤️ using Django REST Framework**

