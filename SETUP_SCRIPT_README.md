# 🚀 Setup Script - Complete Data Initialization

## Overview

This script automatically creates:
- ✅ **Users** (Admin, Test Users, Customers)
- ✅ **Categories** (5 stamp categories)
- ✅ **Services** (8 printing services)
- ✅ **Products** (12 products: stamps + services)

---

## 📋 Quick Start

### **Option 1: Run with Django Shell (Recommended)**

```bash
python manage.py shell < setup_all_data.py
```

### **Option 2: Run in Interactive Shell**

```bash
python manage.py shell
```

Then in the shell:
```python
exec(open('setup_all_data.py').read())
```

### **Option 3: Run as Python Script**

```bash
python setup_all_data.py
```

---

## 📦 What Gets Created

### **1. Users (4 users)**

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | admin123 | Admin/Superuser |
| testuser@example.com | testpass123 | Customer |
| customer1@example.com | customer123 | Customer |
| customer2@example.com | customer123 | Customer |

### **2. Categories (6 categories)**

**Stamp Categories (5):**
1. Dater Stamp Products
2. Handy and Pocket Stamps
3. Heavy Duty Stamps
4. Oval Self Ink Stamps
5. Round Self Ink Stamps

**Service Category (1):**
6. Printing Services (for service products - no documents required)

### **3. Services (8 services)**

1. Screen Printing
2. DTF Printing
3. UV Printing
4. Offset Printing
5. Digital Printing
6. Stamp Manufacturing
7. Signboard & Banner Printing
8. Label & Sticker Printing

### **4. Products (12 products)**

**Stamp Products (9):**
- R-532D Dater Stamp ($75)
- R-532D Shiny ($85, on sale $75)
- Pocket Stamp P-100 ($45)
- Handy Stamp H-200 ($50, on sale $45)
- Heavy Duty Stamp HD-500 ($120)
- Oval Self Ink Stamp OV-100 ($65)
- Oval Self Ink Stamp OV-200 ($80, on sale $70)
- Round Self Ink Stamp RD-100 ($60)
- Round Self Ink Stamp RD-200 ($75)

**Service Products (3):**
- T-Shirt Screen Printing ($25)
- DTF T-Shirt Printing ($30, on sale $25)
- Business Card Printing ($50)
- Flyer Printing ($0.50)

---

## ✅ Features

- **Idempotent**: Safe to run multiple times (won't create duplicates)
- **Complete**: Creates all necessary data for testing
- **Realistic**: Products with prices, descriptions, stock
- **Document Requirements**: Stamp products need documents, services don't

---

## 🔍 Verification

After running the script, verify:

```bash
# Check users
python manage.py shell
>>> from apps.accounts.models import User
>>> User.objects.count()
4

# Check categories
>>> from apps.catalog.models import Category
>>> Category.objects.count()
5

# Check services
>>> from apps.catalog.models import Service
>>> Service.objects.count()
8

# Check products
>>> from apps.catalog.models import Product
>>> Product.objects.count()
12
```

---

## 🧪 Testing After Setup

### **1. Test Login**

```bash
# Admin login
POST /api/v1/auth/login/
{
  "email": "admin@example.com",
  "password": "admin123"
}

# Customer login
POST /api/v1/auth/login/
{
  "email": "testuser@example.com",
  "password": "testpass123"
}
```

### **2. Test Products**

```bash
# Get stamp product (requires documents)
GET /api/v1/products/1/

# Get service product (no documents needed)
GET /api/v1/products/10/
```

### **3. Test Cart & Checkout**

```bash
# Add stamp product to cart (with documents)
POST /api/v1/cart/items/
- product_id: 1
- quantity: 2
- emirates_id: <file>
- trade_license: <file>

# Add service product to cart (no documents)
POST /api/v1/cart/items/
- product_id: 10
- quantity: 1

# Checkout
POST /api/v1/orders/checkout/
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+971501234567",
  "address_line_1": "123 Main Street",
  "city": "Dubai",
  "country": "UAE"
}
```

---

## 🔄 Re-running the Script

The script is **idempotent** - safe to run multiple times:

- ✅ Existing users won't be recreated
- ✅ Existing categories won't be duplicated
- ✅ Existing services won't be duplicated
- ✅ Existing products won't be duplicated

**To reset everything:**

```bash
# Clear all data (careful!)
python manage.py shell
>>> from apps.accounts.models import User
>>> from apps.catalog.models import Category, Service, Product
>>> Product.objects.all().delete()
>>> Category.objects.all().delete()
>>> Service.objects.all().delete()
>>> User.objects.filter(is_superuser=False).delete()
```

Then run the setup script again.

---

## 📝 Customization

To customize the script, edit `setup_all_data.py`:

- **Add more users**: Add to `users_data` list
- **Add more categories**: Add to `categories_data` list
- **Add more services**: Add to `services_data` list
- **Add more products**: Add to `products_data` list

---

## ⚠️ Notes

1. **Passwords**: All test passwords are simple for testing. Change in production!
2. **Documents**: Stamp products require Emirates ID + Trade License
3. **Services**: Service products don't require documents
4. **Stock**: Products have initial stock quantities set
5. **Prices**: All prices in AED

---

## 🐛 Troubleshooting

### **Error: "User already exists"**
- This is normal - script won't recreate existing users
- Check if user exists: `User.objects.filter(email='admin@example.com').exists()`

### **Error: "Category already exists"**
- Normal - script uses `get_or_create` to avoid duplicates
- Safe to run multiple times

### **Error: "No such table"**
- Run migrations first: `python manage.py migrate`

### **Error: "Module not found"**
- Make sure you're in the project root directory
- Activate virtual environment if using one

---

## 📚 Related Scripts

- `create_categories_services.py` - Creates only categories and services
- `setup_product_requirements.py` - Sets up document requirements for products

---

## ✅ Success Output

When successful, you'll see:

```
======================================================================
🚀 COMPLETE SETUP SCRIPT
======================================================================

======================================================================
📝 STEP 1: Creating Users...
======================================================================
✅ Created user: admin@example.com (Admin)
✅ Created user: testuser@example.com (Customer)
...

📊 Users: 4 created, 4 total

======================================================================
📁 STEP 2: Creating Categories...
======================================================================
✅ Created: Dater Stamp Products
...

📊 Categories: 5 created, 5 total

======================================================================
🛠️  STEP 3: Creating Services...
======================================================================
✅ Created: Screen Printing
...

📊 Services: 8 created, 8 total

======================================================================
📦 STEP 4: Creating Products...
======================================================================
✅ Created: R-532D Dater Stamp ($75.00)
...

📊 Products: 12 created, 12 total

======================================================================
✅ SETUP COMPLETE!
======================================================================
```

---

## 🎉 You're Ready!

After running the script, you have:
- ✅ Test users to login with
- ✅ Categories for stamp products
- ✅ Services for printing services
- ✅ Products to test cart and checkout
- ✅ Complete data for end-to-end testing

Happy testing! 🚀

