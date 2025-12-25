"""
Script to set up document requirements for products
Run: python manage.py shell < setup_product_requirements.py
Or: python manage.py shell, then copy-paste this code
"""
from apps.catalog.models import Product, ProductRequirement, Category

# Get all stamp products (custom stamps need documents)
stamp_categories = Category.objects.filter(
    slug__in=[
        'dater-stamp-products',
        'handy-and-pocket-stamps',  # Fixed: was 'handy-pocket-stamps'
        'heavy-duty-stamps',
        'oval-self-ink-stamps',
        'round-self-ink-stamps'
    ]
)

print("=" * 50)
print("Setting up Product Requirements for Custom Stamps")
print("=" * 50)

created_count = 0
updated_count = 0

for category in stamp_categories:
    products = Product.objects.filter(category=category, is_active=True)
    
    for product in products:
        print(f"\n📦 Product: {product.name} (ID: {product.id})")
        
        # Emirates ID - Required
        emirates_id_req, created = ProductRequirement.objects.get_or_create(
            product=product,
            doc_type='EMIRATES_ID',
            defaults={
                'is_required': True,
                'description': 'Upload your Emirates ID for identity verification',
                'order': 1
            }
        )
        if created:
            print("  ✅ Created: Emirates ID (Required)")
            created_count += 1
        else:
            print("  ⚠️  Already exists: Emirates ID")
            updated_count += 1
        
        # Trade License - Required
        trade_license_req, created = ProductRequirement.objects.get_or_create(
            product=product,
            doc_type='TRADE_LICENSE',
            defaults={
                'is_required': True,
                'description': 'Upload your Trade License for business verification',
                'order': 2
            }
        )
        if created:
            print("  ✅ Created: Trade License (Required)")
            created_count += 1
        else:
            print("  ⚠️  Already exists: Trade License")
            updated_count += 1
        
        # Design File - Optional
        design_req, created = ProductRequirement.objects.get_or_create(
            product=product,
            doc_type='DESIGN',
            defaults={
                'is_required': False,
                'description': 'Upload your custom design file (optional)',
                'order': 3
            }
        )
        if created:
            print("  ✅ Created: Design File (Optional)")
            created_count += 1
        else:
            print("  ⚠️  Already exists: Design File")
            updated_count += 1

print("\n" + "=" * 50)
print(f"✅ Setup Complete!")
print(f"   Created: {created_count} requirements")
print(f"   Already existed: {updated_count} requirements")
print("=" * 50)

# Also set up for a specific product if needed
print("\n💡 To set up requirements for a specific product:")
print("   ProductRequirement.objects.create(")
print("       product=Product.objects.get(id=1),")
print("       doc_type='EMIRATES_ID',")
print("       is_required=True")
print("   )")

