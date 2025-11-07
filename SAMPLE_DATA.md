# Sample Data Created! 🎉

## ✅ What Was Created

Your database now contains realistic sample data perfect for testing and development!

## 📊 Data Summary

### Users (21 total)
- **1 Admin User**
  - Username: `admin`
  - Password: `admin123`
  - Email: `admin@example.com`
  - Has superuser access

- **1 Test User**
  - Username: `testuser`
  - Password: `testpass123`
  - Email: `test@example.com`
  - Regular user

- **19 Additional Users**
  - Random realistic names
  - Unique usernames (user0, user1, etc.)
  - Complete profile information
  - Password: `testpass123` for all

### Categories (8 total)
1. **Dater Stamp Products** - Professional dater stamps
2. **Handy and Pocket Stamps** - Compact portable stamps
3. **Heavy Duty Stamps** - Industrial-grade stamps
4. **Oval Self Ink Stamps** - Professional oval stamps
5. **Round Self Ink Stamps** - Circular stamps
6. **Digital Printing** - High-quality digital services
7. **Screen Printing** - Professional screen printing
8. **Office Supplies** - Essential office items

Plus 2 subcategories!

### Products (40 total)
- **10 Complete Products** - With specifications
- **8 Featured Products** - Marked as featured
- **5 Products on Sale** - 20% discount
- **17 Regular Products** - Standard listings

All products have:
- Realistic names and descriptions
- Proper pricing
- Stock quantities
- SKU codes
- Categories assigned

### Shopping Carts (5 total)
- 5 users have active carts
- Each cart has 3 items
- Items from various products
- Quantities vary

### Orders (20 total)
- **6 Pending Orders** - Awaiting confirmation
- **6 Confirmed Orders** - Processing
- **8 Completed Orders** - Delivered & paid

All orders include:
- Customer information
- Shipping address
- Order items
- Realistic totals

## 🔑 Login Credentials

### Admin Access
```
URL: http://localhost:8000/admin/
Username: admin
Password: admin123
```

### Test User API Access
```
Username: testuser
Password: testpass123
```

### All Users
All generated users have password: `testpass123`

## 🚀 Test the Data

### 1. Login to Admin Panel
```
http://localhost:8000/admin/
```
Login with admin credentials and explore:
- View all products
- Process orders
- Manage categories
- View users

### 2. Test API Endpoints

#### Get Products
```bash
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/products/" -Method GET

# Browser
http://localhost:8000/api/products/
```

#### Login as Test User
```bash
$body = @{
    username = "testuser"
    password = "testpass123"
} | ConvertTo-Json

$tokens = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method POST -Body $body -ContentType "application/json"

# Save token
$token = $tokens.access
Write-Host "Token: $token"
```

#### Get User's Cart
```bash
$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/cart/" -Method GET -Headers $headers
```

#### Get User's Orders
```bash
Invoke-RestMethod -Uri "http://localhost:8000/api/orders/" -Method GET -Headers $headers
```

## 📱 API Testing

### Using Swagger UI
1. Go to: http://localhost:8000/api/docs/
2. Click "Authorize" button
3. Login to get token
4. Paste token in format: `Bearer YOUR_TOKEN`
5. Test all endpoints interactively!

## 🔍 Explore the Data

### View Products
```python
python manage.py shell
```

```python
from api.models import Product, Category, Order

# Count products
Product.objects.count()  # 40

# Get featured products
Product.objects.filter(is_featured=True).count()  # 8

# Get products on sale
Product.objects.filter(sale_price__isnull=False).count()  # 5

# View a product
product = Product.objects.first()
print(f"{product.name} - AED {product.current_price}")
```

### View Orders
```python
from api.models import Order

# Get all orders
Order.objects.count()  # 20

# Pending orders
Order.objects.filter(status='pending').count()  # 6

# View an order
order = Order.objects.first()
print(f"Order {order.order_number}")
print(f"Customer: {order.full_name}")
print(f"Total: AED {order.total}")
print(f"Items: {order.items.count()}")
```

## 🗑️ Clear and Regenerate

### Clear All Sample Data
```bash
python manage.py create_sample_data --clear
```

This will delete all data except superusers.

### Regenerate with Custom Amounts
```bash
# Create more data
python manage.py create_sample_data --users 50 --products 100 --orders 50

# Create less data
python manage.py create_sample_data --users 5 --products 10 --orders 5
```

## 📈 Data Statistics

To view current statistics:
```bash
python manage.py shell
```

```python
from api.models import User, Product, Category, Order, Cart

print(f"Users: {User.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Categories: {Category.objects.count()}")
print(f"Orders: {Order.objects.count()}")
print(f"Carts: {Cart.objects.count()}")
```

## 🎯 What to Do Next

### 1. Explore Admin Panel
- View and edit products
- Process orders
- Manage inventory
- View customer information

### 2. Test API Endpoints
- Register new users
- Add products to cart
- Create orders
- Search products

### 3. Build Your Frontend
- Connect your Next.js app
- Fetch products
- Implement cart functionality
- Handle checkout

### 4. Customize Data
- Add more categories
- Upload product images
- Create custom products
- Process sample orders

## 💡 Pro Tips

### Quick Login Test
```bash
# Test login works
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"testpass123\"}"
```

### View Featured Products
```bash
curl http://localhost:8000/api/products/featured/
```

### Search Products
```bash
curl "http://localhost:8000/api/products/search/?q=stamp"
```

## 🔄 Reset Database

If you want to start fresh:

```bash
# Delete database
del db.sqlite3  # Windows
# rm db.sqlite3  # Mac/Linux

# Recreate database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Generate sample data
python manage.py create_sample_data
```

## 📊 Sample Data Quality

All generated data is:
- ✅ **Realistic** - Uses Faker for authentic-looking data
- ✅ **Consistent** - Follows proper relationships
- ✅ **Complete** - All required fields populated
- ✅ **Diverse** - Various product types, order statuses
- ✅ **Test-Ready** - Perfect for development and testing

## 🎉 Success!

You now have a fully populated database ready for:
- Testing API endpoints
- Developing frontend
- Demonstrating features
- Training users
- Performance testing

**Start exploring at: http://localhost:8000/admin/**

Login with: `admin` / `admin123`

