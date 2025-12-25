"""
Script to create all categories and services
Run: python manage.py shell < create_categories_services.py
Or: python manage.py shell, then copy-paste this code
"""
from apps.catalog.models import Category, Service

# ============ CREATE CATEGORIES ============
print("=" * 50)
print("Creating Categories...")
print("=" * 50)

categories = [
    {
        "name": "Dater Stamp Products",
        "slug": "dater-stamp-products",
        "description": "Professional dater stamps with date, company name and received text",
        "order": 1
    },
    {
        "name": "Handy and Pocket Stamps",
        "slug": "handy-pocket-stamps",
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
for cat_data in categories:
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

# ============ CREATE SERVICES ============
print("=" * 50)
print("Creating Services...")
print("=" * 50)

services = [
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
for service_data in services:
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

# ============ SUMMARY ============
print("=" * 50)
print("✅ COMPLETE!")
print("=" * 50)
print(f"📁 Categories: {Category.objects.count()}")
print(f"🛠️  Services: {Service.objects.count()}")
print("\n🎉 All categories and services are ready!")

