# 📄 Document Requirements Explained

## ✅ Documents Required for PRODUCTS (Custom Stamps)

**Documents are required for PRODUCTS, NOT for SERVICES.**

---

## Products vs Services

### Products (Custom Stamps) - Documents Required ✅

**Examples:**
- Dater Stamps
- Pocket Stamps
- Heavy Duty Stamps
- Self-Ink Stamps

**Required Documents:**
- ✅ **Emirates ID** - Required
- ✅ **Trade License** - Required
- ⭕ **Design File** - Optional

**Why?**
- UAE regulations require identity verification for custom stamps
- Business stamps need trade license proof
- Ensures legitimate customers

---

### Services (Printing Services) - No Documents Required ❌

**Examples:**
- Screen Printing
- DTF Printing
- Banners
- Business Cards
- Flyers
- Stickers

**Required Documents:**
- ❌ **Emirates ID** - NOT required
- ❌ **Trade License** - NOT required
- ⭕ **Design File** - Only if customer wants custom design

**Why?**
- Services are simpler transactions
- No regulatory requirements
- Just need design files for printing

---

## How It Works in the System

### Product Requirements Model

```python
ProductRequirement
├── product (ForeignKey to Product)
├── doc_type (EMIRATES_ID, TRADE_LICENSE, DESIGN, OTHER)
├── is_required (True/False)
└── description
```

**Key Point:** Requirements are linked to **Products**, not Services!

### When Adding to Cart

**For Products (Stamps):**
```bash
# 1. Add product to cart
POST /api/v1/cart/items/
{"product_id": 1, "quantity": 2}

# 2. Upload required documents
POST /api/v1/cart/items/1/documents/
{"doc_type": "EMIRATES_ID", "file": ...}

POST /api/v1/cart/items/1/documents/
{"doc_type": "TRADE_LICENSE", "file": ...}

# 3. Checkout validates documents
POST /api/v1/orders/checkout/
# ✅ Will fail if documents missing
```

**For Services (Printing):**
```bash
# 1. Add service to cart (if services are products)
POST /api/v1/cart/items/
{"product_id": 10, "quantity": 1}

# 2. Upload design file (optional)
POST /api/v1/cart/items/10/documents/
{"doc_type": "DESIGN", "file": ...}

# 3. Checkout (no document validation needed)
POST /api/v1/orders/checkout/
# ✅ Works without Emirates ID or Trade License
```

---

## Configuration

### Setting Up Product Requirements

**For Custom Stamps (Products):**
```python
# Create requirement for a stamp product
ProductRequirement.objects.create(
    product=stamp_product,
    doc_type='EMIRATES_ID',
    is_required=True,
    description='Upload your Emirates ID'
)

ProductRequirement.objects.create(
    product=stamp_product,
    doc_type='TRADE_LICENSE',
    is_required=True,
    description='Upload your Trade License'
)
```

**For Printing Services (Products):**
```python
# No requirements needed, or only optional design
ProductRequirement.objects.create(
    product=printing_service_product,
    doc_type='DESIGN',
    is_required=False,  # Optional!
    description='Upload your design file (optional)'
)
```

---

## Summary

| Item Type | Emirates ID | Trade License | Design File |
|-----------|-------------|---------------|-------------|
| **Custom Stamps (Products)** | ✅ Required | ✅ Required | ⭕ Optional |
| **Printing Services** | ❌ Not Required | ❌ Not Required | ⭕ Optional |

---

## Important Notes

1. **Requirements are per PRODUCT** - Each product can have different requirements
2. **Services don't need documents** - Unless you configure them as products with requirements
3. **Checkout validates** - Only checks requirements for products that have them
4. **Flexible system** - You can configure any product to require or not require documents

---

**Bottom line: Documents are for custom stamps (products), not for printing services!** 🎯

