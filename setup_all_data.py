"""
Complete Setup Script
Creates users, categories, services, and products automatically

Usage:
    python manage.py shell < setup_all_data.py
Or:
    python manage.py shell
    >>> exec(open('setup_all_data.py').read())
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.catalog.models import Category, Service, Product
from django.contrib.auth.hashers import make_password

print("=" * 70)
print("🚀 COMPLETE SETUP SCRIPT")
print("=" * 70)
print()

# ============================================================================
# STEP 1: CREATE USERS
# ============================================================================
print("=" * 70)
print("📝 STEP 1: Creating Users...")
print("=" * 70)

users_data = [
    {
        "email": "admin@example.com",
        "username": "admin",
        "password": "admin123",
        "first_name": "Admin",
        "last_name": "User",
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
        "phone": "+971501234567",
        "company_name": "Admin Company"
    },
    {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "is_staff": False,
        "is_superuser": False,
        "is_active": True,
        "phone": "+971501234568",
        "company_name": "Test Company"
    },
    {
        "email": "customer1@example.com",
        "username": "customer1",
        "password": "customer123",
        "first_name": "John",
        "last_name": "Doe",
        "is_staff": False,
        "is_superuser": False,
        "is_active": True,
        "phone": "+971501234569",
        "company_name": "Doe Enterprises"
    },
    {
        "email": "customer2@example.com",
        "username": "customer2",
        "password": "customer123",
        "first_name": "Jane",
        "last_name": "Smith",
        "is_staff": False,
        "is_superuser": False,
        "is_active": True,
        "phone": "+971501234570",
        "company_name": "Smith Corp"
    }
]

created_users = 0
for user_data in users_data:
    password = user_data.pop('password')
    email = user_data['email']
    
    user, created = User.objects.get_or_create(
        email=email,
        defaults=user_data
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"✅ Created user: {email} ({'Admin' if user.is_superuser else 'Customer'})")
        created_users += 1
    else:
        print(f"⚠️  User already exists: {email}")

print(f"\n📊 Users: {created_users} created, {User.objects.count()} total\n")

# ============================================================================
# STEP 2: CREATE CATEGORIES
# ============================================================================
print("=" * 70)
print("📁 STEP 2: Creating Categories...")
print("=" * 70)

categories_data = [
    {
        "name": "Dater Stamp Products",
        "slug": "dater-stamp-products",
        "description": "Professional dater stamps with date, company name and received text",
        "order": 1
    },
    {
        "name": "Handy and Pocket Stamps",
        "slug": "handy-and-pocket-stamps",
        "description": "Compact pocket-sized stamps for on-the-go use",
        "order": 2
    },
    {
        "name": "Heavy Duty Stamps",
        "slug": "heavy-duty-stamps",
        "description": "Heavy-duty professional stamps for high-volume use",
        "order": 3
    },
    {
        "name": "Oval Self Ink Stamps",
        "slug": "oval-self-ink-stamps",
        "description": "Professional oval self-inking stamps in various colors",
        "order": 4
    },
    {
        "name": "Round Self Ink Stamps",
        "slug": "round-self-ink-stamps",
        "description": "Professional round self-inking stamps in various colors",
        "order": 5
    }
]

created_categories = 0
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        slug=cat_data["slug"],
        defaults=cat_data
    )
    if created:
        print(f"✅ Created: {category.name}")
        created_categories += 1
    else:
        print(f"⚠️  Already exists: {category.name}")

print(f"\n📊 Categories: {created_categories} created, {Category.objects.count()} total\n")

# ============================================================================
# STEP 3: CREATE SERVICES
# ============================================================================
print("=" * 70)
print("🛠️  STEP 3: Creating Services...")
print("=" * 70)

services_data = [
    {
        "name": "Screen Printing",
        "slug": "screen-printing",
        "description": "High-quality screen printing services for various materials",
        "order": 1
    },
    {
        "name": "DTF Printing",
        "slug": "dtf-printing",
        "description": "Direct to film printing for vibrant, durable prints",
        "order": 2
    },
    {
        "name": "UV Printing",
        "slug": "uv-printing",
        "description": "UV printing for high-resolution, weather-resistant prints",
        "order": 3
    },
    {
        "name": "Offset Printing",
        "slug": "offset-printing",
        "description": "Professional offset printing for large volume orders",
        "order": 4
    },
    {
        "name": "Digital Printing",
        "slug": "digital-printing",
        "description": "Fast digital printing for small to medium runs",
        "order": 5
    },
    {
        "name": "Stamp Manufacturing",
        "slug": "stamp-manufacturing",
        "description": "Custom rubber stamps, self-inking stamps, and date stamps",
        "order": 6
    },
    {
        "name": "Signboard & Banner Printing",
        "slug": "signboard-banner-printing",
        "description": "Large format printing for banners, signs, and displays",
        "order": 7
    },
    {
        "name": "Label & Sticker Printing",
        "slug": "label-sticker-printing",
        "description": "Custom labels, stickers, and decals",
        "order": 8
    }
]

created_services = 0
for service_data in services_data:
    service, created = Service.objects.get_or_create(
        slug=service_data["slug"],
        defaults=service_data
    )
    if created:
        print(f"✅ Created: {service.name}")
        created_services += 1
    else:
        print(f"⚠️  Already exists: {service.name}")

print(f"\n📊 Services: {created_services} created, {Service.objects.count()} total\n")

# ============================================================================
# STEP 4: CREATE PRODUCTS
# ============================================================================
print("=" * 70)
print("📦 STEP 4: Creating Products...")
print("=" * 70)

# Get categories (for stamp products - these require documents)
dater_category = Category.objects.get(slug="dater-stamp-products")
handy_category = Category.objects.get(slug="handy-and-pocket-stamps")
heavy_category = Category.objects.get(slug="heavy-duty-stamps")
oval_category = Category.objects.get(slug="oval-self-ink-stamps")
round_category = Category.objects.get(slug="round-self-ink-stamps")

# Get services (for service products - these don't require documents)
screen_service = Service.objects.get(slug="screen-printing")
dtf_service = Service.objects.get(slug="dtf-printing")
digital_service = Service.objects.get(slug="digital-printing")
uv_service = Service.objects.get(slug="uv-printing")
offset_service = Service.objects.get(slug="offset-printing")
signboard_service = Service.objects.get(slug="signboard-banner-printing")
label_service = Service.objects.get(slug="label-sticker-printing")

# Create a generic category for service products
# (Category is required by Product model, but this won't trigger document requirements
#  because it's not in the stamp_category_slugs list)
service_category, _ = Category.objects.get_or_create(
    slug="printing-services",
    defaults={
        "name": "Printing Services",
        "description": "Professional printing services - no documents required",
        "order": 10
    }
)

products_data = [
    # ========================================================================
    # STAMP PRODUCTS (Have Category, NO Service) - Require Documents
    # ========================================================================
    
    # Dater Stamp Products
    {
        "name": "R-532D Dater Stamp",
        "slug": "r-532d-dater-stamp",
        "category": dater_category,  # Has category
        "service": None,  # NO service
        "description": "Professional dater stamp with date, company name, and received text. Perfect for office use.",
        "short_description": "Professional dater stamp for office use",
        "price": 75.00,
        "sale_price": None,
        "stock_quantity": 50,
        "sku": "DST-001",
        "is_active": True,
        "is_featured": True
    },
    {
        "name": "R-532D Shiny",
        "slug": "r-532d-shiny",
        "category": dater_category,
        "service": None,
        "description": "Shiny finish dater stamp with premium quality. Includes date, company name, and received text.",
        "short_description": "Premium shiny finish dater stamp",
        "price": 85.00,
        "sale_price": 75.00,
        "stock_quantity": 30,
        "sku": "DST-002",
        "is_active": True,
        "is_featured": False
    },
    # Handy and Pocket Stamps (Category, NO Service)
    {
        "name": "Pocket Stamp P-100",
        "slug": "pocket-stamp-p-100",
        "category": handy_category,
        "service": None,
        "description": "Compact pocket-sized stamp perfect for on-the-go professionals. Lightweight and portable.",
        "short_description": "Compact pocket-sized stamp",
        "price": 45.00,
        "sale_price": None,
        "stock_quantity": 100,
        "sku": "PST-001",
        "is_active": True,
        "is_featured": True
    },
    {
        "name": "Handy Stamp H-200",
        "slug": "handy-stamp-h-200",
        "category": handy_category,
        "service": None,
        "description": "Handy stamp with ergonomic design. Easy to use and carry.",
        "short_description": "Ergonomic handy stamp",
        "price": 50.00,
        "sale_price": 45.00,
        "stock_quantity": 75,
        "sku": "PST-002",
        "is_active": True,
        "is_featured": False
    },
    # Heavy Duty Stamps (Category, NO Service)
    {
        "name": "Heavy Duty Stamp HD-500",
        "slug": "heavy-duty-stamp-hd-500",
        "category": heavy_category,
        "service": None,
        "description": "Heavy-duty professional stamp designed for high-volume use. Durable and long-lasting.",
        "short_description": "Heavy-duty stamp for high-volume use",
        "price": 120.00,
        "sale_price": None,
        "stock_quantity": 25,
        "sku": "HDS-001",
        "is_active": True,
        "is_featured": True
    },
    # Oval Self Ink Stamps (Category, NO Service)
    {
        "name": "Oval Self Ink Stamp OV-100",
        "slug": "oval-self-ink-stamp-ov-100",
        "category": oval_category,
        "service": None,
        "description": "Professional oval self-inking stamp available in multiple colors. Clean and professional appearance.",
        "short_description": "Oval self-inking stamp in multiple colors",
        "price": 65.00,
        "sale_price": None,
        "stock_quantity": 60,
        "sku": "OVS-001",
        "is_active": True,
        "is_featured": True
    },
    {
        "name": "Oval Self Ink Stamp OV-200",
        "slug": "oval-self-ink-stamp-ov-200",
        "category": oval_category,
        "service": None,
        "description": "Premium oval self-inking stamp with enhanced durability.",
        "short_description": "Premium oval self-inking stamp",
        "price": 80.00,
        "sale_price": 70.00,
        "stock_quantity": 40,
        "sku": "OVS-002",
        "is_active": True,
        "is_featured": False
    },
    # Round Self Ink Stamps (Category, NO Service)
    {
        "name": "Round Self Ink Stamp RD-100",
        "slug": "round-self-ink-stamp-rd-100",
        "category": round_category,
        "service": None,
        "description": "Professional round self-inking stamp. Perfect for official documents.",
        "short_description": "Round self-inking stamp for official use",
        "price": 60.00,
        "sale_price": None,
        "stock_quantity": 80,
        "sku": "RDS-001",
        "is_active": True,
        "is_featured": True
    },
    {
        "name": "Round Self Ink Stamp RD-200",
        "slug": "round-self-ink-stamp-rd-200",
        "category": round_category,
        "service": None,
        "description": "Premium round self-inking stamp with multiple color options.",
        "short_description": "Premium round self-inking stamp",
        "price": 75.00,
        "sale_price": None,
        "stock_quantity": 50,
        "sku": "RDS-002",
        "is_active": True,
        "is_featured": False
    },
    # ========================================================================
    # SERVICE PRODUCTS (Have Service, Generic Category) - NO Documents Required
    # ========================================================================
    
    {
        "name": "T-Shirt Screen Printing",
        "slug": "t-shirt-screen-printing",
        "category": service_category,  # Generic category (required by model, but not a stamp category)
        "service": screen_service,  # Has service
        "description": "High-quality screen printing on t-shirts. Custom designs available. Minimum order: 10 pieces.",
        "short_description": "Screen printing on t-shirts",
        "price": 25.00,
        "sale_price": None,
        "stock_quantity": 0,  # Services don't track inventory
        "sku": "SRV-001",
        "is_active": True,
        "is_featured": True
    },
    {
        "name": "DTF T-Shirt Printing",
        "slug": "dtf-t-shirt-printing",
        "category": service_category,  # Generic category
        "service": dtf_service,  # Has service
        "description": "Direct to film printing on t-shirts. Vibrant colors and durable prints. Minimum order: 5 pieces.",
        "short_description": "DTF printing on t-shirts",
        "price": 30.00,
        "sale_price": 25.00,
        "stock_quantity": 0,
        "sku": "SRV-002",
        "is_active": True,
        "is_featured": True
    },
    {
        "name": "Business Card Printing",
        "slug": "business-card-printing",
        "category": service_category,  # Generic category
        "service": digital_service,  # Has service
        "description": "Professional business card printing. Multiple paper options and finishes available.",
        "short_description": "Professional business card printing",
        "price": 50.00,
        "sale_price": None,
        "stock_quantity": 0,
        "sku": "SRV-003",
        "is_active": True,
        "is_featured": False
    },
    {
        "name": "Flyer Printing",
        "slug": "flyer-printing",
        "category": service_category,  # Generic category
        "service": digital_service,  # Has service
        "description": "High-quality flyer printing. Various sizes and paper types available.",
        "short_description": "High-quality flyer printing",
        "price": 0.50,
        "sale_price": None,
        "stock_quantity": 0,
        "sku": "SRV-004",
        "is_active": True,
        "is_featured": False
    },
    {
        "name": "UV Banner Printing",
        "slug": "uv-banner-printing",
        "category": service_category,  # Generic category
        "service": uv_service,  # Has service
        "description": "UV printing for banners. Weather-resistant and vibrant colors. Perfect for outdoor use.",
        "short_description": "UV printing for outdoor banners",
        "price": 15.00,
        "sale_price": None,
        "stock_quantity": 0,
        "sku": "SRV-005",
        "is_active": True,
        "is_featured": True
    },
    {
        "name": "Offset Brochure Printing",
        "slug": "offset-brochure-printing",
        "category": service_category,  # Generic category
        "service": offset_service,  # Has service
        "description": "Professional offset printing for brochures. High quality for large volume orders.",
        "short_description": "Offset printing for brochures",
        "price": 0.30,
        "sale_price": None,
        "stock_quantity": 0,
        "sku": "SRV-006",
        "is_active": True,
        "is_featured": False
    },
    {
        "name": "Signboard Printing",
        "slug": "signboard-printing",
        "category": service_category,  # Generic category
        "service": signboard_service,  # Has service
        "description": "Large format signboard printing. Durable and weather-resistant materials.",
        "short_description": "Large format signboard printing",
        "price": 50.00,
        "sale_price": None,
        "stock_quantity": 0,
        "sku": "SRV-007",
        "is_active": True,
        "is_featured": True
    },
    {
        "name": "Custom Label Printing",
        "slug": "custom-label-printing",
        "category": service_category,  # Generic category
        "service": label_service,  # Has service
        "description": "Custom label and sticker printing. Various sizes and materials available.",
        "short_description": "Custom label and sticker printing",
        "price": 0.20,
        "sale_price": None,
        "stock_quantity": 0,
        "sku": "SRV-008",
        "is_active": True,
        "is_featured": False
    }
]

created_products = 0
for product_data in products_data:
    slug = product_data["slug"]
    product, created = Product.objects.get_or_create(
        slug=slug,
        defaults=product_data
    )
    if created:
        print(f"✅ Created: {product.name} (${product.price})")
        created_products += 1
    else:
        print(f"⚠️  Already exists: {product.name}")

print(f"\n📊 Products: {created_products} created, {Product.objects.count()} total\n")

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 70)
print("✅ SETUP COMPLETE!")
print("=" * 70)
print()
# Count products by type
stamp_products = Product.objects.filter(service__isnull=True).count()
service_products = Product.objects.filter(service__isnull=False).count()

print("📊 Summary:")
print(f"   👥 Users: {User.objects.count()}")
print(f"   📁 Categories: {Category.objects.count()} (5 stamp categories + 1 service category)")
print(f"   🛠️  Services: {Service.objects.count()}")
print(f"   📦 Products: {Product.objects.count()}")
print(f"      - Stamp Products (have category, no service): {stamp_products}")
print(f"      - Service Products (have service): {service_products}")
print()
print("🔑 Test Credentials:")
print("   Admin:")
print("     Email: admin@example.com")
print("     Password: admin123")
print()
print("   Customer:")
print("     Email: testuser@example.com")
print("     Password: testpass123")
print()
print("📝 Notes:")
print("   - Stamp Products: Have category, NO service → Require documents (Emirates ID, Trade License)")
print("   - Service Products: Have service, generic category → NO documents required")
print("   - You can now test the complete flow!")
print()
print("=" * 70)

