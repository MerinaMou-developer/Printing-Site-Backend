# Frontend Requirements Handling

## Backend Changes

✅ **Removed automatic requirement creation**
- Backend no longer auto-creates `ProductRequirement` records
- Frontend handles requirement display based on category

---

## Frontend Implementation

### How to Show Requirements

**Check product category to determine if requirements are needed:**

```javascript
// Stamp categories that need documents
const STAMP_CATEGORIES = [
  'dater-stamp-products',
  'handy-and-pocket-stamps',
  'heavy-duty-stamps',
  'oval-self-ink-stamps',
  'round-self-ink-stamps'
];

// Check if product needs documents
function needsDocuments(product) {
  return STAMP_CATEGORIES.includes(product.category_slug);
}

// Show requirements UI if needed
if (needsDocuments(product)) {
  // Show document upload fields:
  // - Emirates ID (required)
  // - Trade License (required)
  // - Design (optional)
} else {
  // Service product - no documents needed
  // Only show optional design upload
}
```

---

## API Response

**Product API still returns category info:**

```json
{
  "id": 1,
  "name": "Shiny R-532D",
  "category": 1,
  "category_name": "Dater Stamp Products",
  "category_slug": "dater-stamp-products",
  "requirements": []  // Empty - frontend handles based on category
}
```

**Frontend logic:**
- If `category_slug` is in stamp categories → Show document fields
- If `category_slug` is service category → Don't show document fields

---

## Document Upload

**Still works the same:**
- `POST /api/v1/cart/items/{id}/documents/` - Upload single document
- `POST /api/v1/cart/items/{id}/documents/bulk/` - Upload multiple documents

**Checkout validation:**
- Backend still validates if documents are uploaded
- But requirements are determined by category, not database records

---

## Summary

✅ **Backend:** No automatic requirement creation
✅ **Frontend:** Check category to show/hide requirements
✅ **Upload:** Still works the same way
✅ **Validation:** Backend validates based on category

**Frontend has full control!** 🎉


