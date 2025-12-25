# 🛒 Frontend Checkout Flow - After Cart

## Complete Flow: Cart → Checkout → Order

---

## 📋 Step-by-Step Frontend Flow

### **Step 1: User Views Cart** ✅
**API Call:**
```javascript
GET /api/v1/cart/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": 1,
  "items": [
    {
      "id": 5,
      "product": {
        "id": 1,
        "name": "Shiny R-532D",
        "category_slug": "dater-stamp-products",  // ← Check this!
        "price": "75.00"
      },
      "quantity": 2,
      "price": "75.00",
      "total": "150.00"
    }
  ],
  "subtotal": "150.00",
  "total": "150.00"
}
```

**Frontend Action:**
- Display cart items
- Show product details, quantities, prices
- Calculate and display totals

---

### **Step 2: Check Document Requirements** 📄

**For EACH cart item, check if documents are needed:**

```javascript
// Frontend logic
const STAMP_CATEGORIES = [
  'dater-stamp-products',
  'handy-and-pocket-stamps',
  'heavy-duty-stamps',
  'oval-self-ink-stamps',
  'round-self-ink-stamps'
];

function needsDocuments(cartItem) {
  return STAMP_CATEGORIES.includes(cartItem.product.category_slug);
}

// Check each item
cart.items.forEach(item => {
  if (needsDocuments(item)) {
    // Show document upload UI for this item
    showDocumentUpload(item);
  }
});
```

**API Call to Check Requirements Status:**
```javascript
GET /api/v1/cart/items/{item_id}/requirements/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "cart_item_id": 5,
  "product_id": 1,
  "product_name": "Shiny R-532D",
  "requirements": [
    {
      "doc_type": "EMIRATES_ID",
      "doc_type_display": "Emirates ID",
      "is_required": true,
      "description": "Upload your Emirates ID",
      "is_uploaded": false,  // ← Check this!
      "uploaded_document": null
    },
    {
      "doc_type": "TRADE_LICENSE",
      "doc_type_display": "Trade License",
      "is_required": true,
      "description": "Upload your Trade License",
      "is_uploaded": true,  // ← Already uploaded
      "uploaded_document": {
        "id": 10,
        "file": "/media/cart-documents/...",
        "file_name": "trade_license.pdf"
      }
    }
  ],
  "all_required_uploaded": false  // ← Important!
}
```

**Frontend Action:**
- Show document upload UI for items that need documents
- Display which documents are uploaded/missing
- Show validation status (✅ uploaded / ❌ missing)

---

### **Step 3: Upload Required Documents** 📤

**Option A: Upload Documents When Adding to Cart (Recommended - One API Call)**
```javascript
POST /api/v1/cart/items/
Authorization: Bearer {token}
Content-Type: multipart/form-data

FormData:
  - product_id: 1
  - quantity: 4
  - emirates_id: <file>        // Optional
  - trade_license: <file>       // Optional
  - design: <file>              // Optional
```

**Example with JavaScript:**
```javascript
const formData = new FormData();
formData.append('product_id', 1);
formData.append('quantity', 4);
formData.append('emirates_id', emiratesIdFile);
formData.append('trade_license', tradeLicenseFile);
formData.append('design', designFile);  // Optional

const response = await fetch('/api/v1/cart/items/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});
```

**Response:**
```json
{
  "message": "Item added to cart successfully! 2 document(s) uploaded.",
  "uploaded_documents": [
    {
      "id": 11,
      "doc_type": "EMIRATES_ID",
      "file": "/media/cart-documents/...",
      "file_name": "emirates_id.pdf",
      "file_size": 245678
    },
    {
      "id": 12,
      "doc_type": "TRADE_LICENSE",
      "file": "/media/cart-documents/...",
      "file_name": "trade_license.pdf",
      "file_size": 312456
    }
  ],
  "cart": {
    "id": 1,
    "items": [...],
    "subtotal": "300.00"
  }
}
```

**Option B: Upload Documents After Adding to Cart**
```javascript
POST /api/v1/cart/items/{item_id}/documents/
Authorization: Bearer {token}
Content-Type: multipart/form-data

FormData:
  - doc_type: "EMIRATES_ID"  // or "TRADE_LICENSE" or "DESIGN"
  - file: <file>
```

**Option C: Upload Multiple Documents at Once**
```javascript
POST /api/v1/cart/items/{item_id}/documents/bulk/
Authorization: Bearer {token}
Content-Type: multipart/form-data

FormData:
  - emirates_id: <file>
  - trade_license: <file>
  - design: <file>  // Optional
```

**Response:**
```json
{
  "message": "Uploaded 2 document(s)",
  "uploaded_documents": [
    {
      "id": 11,
      "doc_type": "EMIRATES_ID",
      "file": "/media/cart-documents/...",
      "file_name": "emirates_id.pdf",
      "file_size": 245678
    },
    {
      "id": 12,
      "doc_type": "TRADE_LICENSE",
      "file": "/media/cart-documents/...",
      "file_name": "trade_license.pdf",
      "file_size": 312456
    }
  ]
}
```

**Frontend Action:**
- Show upload progress
- Update UI to show uploaded documents
- Re-check requirements status after upload

---

### **Step 4: Validate All Requirements Before Checkout** ✅

**Before showing checkout button, validate:**

```javascript
async function canProceedToCheckout(cart) {
  for (const item of cart.items) {
    if (needsDocuments(item)) {
      // Check requirements status
      const response = await fetch(
        `/api/v1/cart/items/${item.id}/requirements/`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      );
      const data = await response.json();
      
      if (!data.all_required_uploaded) {
        return {
          canProceed: false,
          missingItems: [{
            product: item.product.name,
            missingDocs: data.requirements
              .filter(r => r.is_required && !r.is_uploaded)
              .map(r => r.doc_type_display)
          }]
        };
      }
    }
  }
  return { canProceed: true };
}
```

**Frontend Action:**
- Disable checkout button if documents missing
- Show warning message: "Please upload all required documents"
- Highlight items with missing documents

---

### **Step 5: Show Checkout Form** 📝

**Display checkout form with:**
- Billing Information (required)
  - First Name
  - Last Name
  - Email
  - Phone
  - Company Name (optional)

- Shipping Address (required)
  - Address Line 1
  - Address Line 2 (optional)
  - City
  - State (optional)
  - Country
  - Postal Code (optional)

- Order Notes (optional)

---

### **Step 6: Submit Checkout** 🚀

**API Call:**
```javascript
POST /api/v1/orders/checkout/
Authorization: Bearer {token}
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+971501234567",
  "company_name": "My Company",  // Optional
  "address_line_1": "123 Main Street",
  "address_line_2": "Building 5",  // Optional
  "city": "Dubai",
  "state": "Dubai",  // Optional
  "country": "UAE",
  "postal_code": "12345",  // Optional
  "order_notes": "Please deliver before 5 PM"  // Optional
}
```

**Success Response (201):**
```json
{
  "id": 1,
  "order_number": "ORD-2025-001",
  "status": "pending",
  "payment_status": "pending",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+971501234567",
  "total": "150.00",
  "subtotal": "150.00",
  "shipping_cost": "0.00",
  "tax": "0.00",
  "items": [
    {
      "id": 1,
      "product": 1,
      "product_name": "Shiny R-532D",
      "quantity": 2,
      "price": "75.00",
      "total": "150.00"
    }
  ],
  "documents": [
    {
      "id": 1,
      "doc_type": "EMIRATES_ID",
      "file": "/media/orders/2025/12/emirates_id.pdf",
      "file_name": "emirates_id.pdf"
    },
    {
      "id": 2,
      "doc_type": "TRADE_LICENSE",
      "file": "/media/orders/2025/12/trade_license.pdf",
      "file_name": "trade_license.pdf"
    }
  ],
  "created_at": "2025-12-15T10:30:00Z"
}
```

**Error Response - Missing Documents (400):**
```json
{
  "error": "Missing required documents",
  "missing_documents": [
    {
      "product_id": 1,
      "product_name": "Shiny R-532D",
      "missing_document": "Emirates ID",
      "doc_type": "EMIRATES_ID"
    }
  ],
  "message": "Please upload all required documents before checkout"
}
```

**Error Response - Empty Cart (400):**
```json
{
  "error": "Cart is empty"
}
```

**Frontend Action:**
- Show loading spinner during checkout
- On success: Redirect to order confirmation page
- On error: Display error message and highlight missing documents
- Clear cart UI (backend clears cart automatically)

---

### **Step 7: Order Confirmation Page** 🎉

**Display order details:**
- Order Number (important!)
- Order Status
- Items ordered
- Total amount
- Shipping address
- Documents uploaded

**Optional: Get Full Order Details**
```javascript
GET /api/v1/orders/{order_id}/
Authorization: Bearer {token}
```

**Frontend Action:**
- Show success message
- Display order summary
- Provide order number for tracking
- Show "View Orders" button

---

### **Step 8: View Orders** 📋

**API Call:**
```javascript
GET /api/v1/orders/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "order_number": "ORD-2025-001",
      "full_name": "John Doe",
      "email": "john@example.com",
      "status": "pending",
      "payment_status": "pending",
      "total": "150.00",
      "items_count": 1,
      "created_at": "2025-12-15T10:30:00Z"
    }
  ]
}
```

**Frontend Action:**
- List all user orders
- Show order status, date, total
- Link to order details page

---

## 🔄 Complete Flow Diagram

```
┌─────────────────┐
│   View Cart     │
│  GET /cart/     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Check Each Item         │
│ Needs Documents?        │
│ (Check category_slug)   │
└────────┬────────────────┘
         │
         ├─ YES (Stamp Product)
         │  └─► Show Document Upload UI
         │      └─► Upload Documents
         │          POST /cart/items/{id}/documents/bulk/
         │
         └─ NO (Service Product)
            └─► No documents needed
                │
                ▼
┌─────────────────────────┐
│ Validate All            │
│ Requirements Uploaded   │
│ GET /cart/items/{id}/   │
│     requirements/       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Show Checkout Form     │
│ (Billing + Shipping)   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Submit Checkout        │
│ POST /orders/checkout/ │
└────────┬────────────────┘
         │
         ├─ Success (201)
         │  └─► Order Created
         │      └─► Show Confirmation
         │          └─► Redirect to Orders
         │
         └─ Error (400)
            ├─ Missing Documents
            │  └─► Show Error
            │      └─► Go Back to Upload
            │
            └─ Empty Cart
               └─► Show Error
```

---

## 🎯 Key Frontend Logic

### **1. Determine if Documents Needed**
```javascript
const STAMP_CATEGORIES = [
  'dater-stamp-products',
  'handy-and-pocket-stamps',
  'heavy-duty-stamps',
  'oval-self-ink-stamps',
  'round-self-ink-stamps'
];

function needsDocuments(product) {
  return STAMP_CATEGORIES.includes(product.category_slug);
}
```

### **2. Validate Before Checkout**
```javascript
async function validateCheckout(cart) {
  const validationErrors = [];
  
  for (const item of cart.items) {
    if (needsDocuments(item.product)) {
      const res = await fetch(`/api/v1/cart/items/${item.id}/requirements/`);
      const data = await res.json();
      
      if (!data.all_required_uploaded) {
        const missing = data.requirements
          .filter(r => r.is_required && !r.is_uploaded)
          .map(r => r.doc_type_display);
        
        validationErrors.push({
          product: item.product.name,
          missing: missing
        });
      }
    }
  }
  
  return validationErrors;
}
```

### **3. Handle Checkout Response**
```javascript
async function handleCheckout(formData) {
  try {
    const response = await fetch('/api/v1/orders/checkout/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });
    
    if (response.status === 201) {
      const order = await response.json();
      // Success! Redirect to confirmation
      router.push(`/orders/${order.id}/confirmation`);
    } else if (response.status === 400) {
      const error = await response.json();
      
      if (error.error === 'Missing required documents') {
        // Show missing documents error
        showMissingDocumentsError(error.missing_documents);
      } else {
        // Show other validation errors
        showValidationErrors(error);
      }
    }
  } catch (error) {
    showError('Network error. Please try again.');
  }
}
```

---

## 📱 UI/UX Recommendations

### **Cart Page:**
- ✅ Show document upload status for each item
- ✅ Highlight items with missing documents
- ✅ Show "Upload Documents" button for stamp products
- ✅ Disable checkout if documents missing

### **Checkout Page:**
- ✅ Show cart summary
- ✅ Show document upload status
- ✅ Validate form before submission
- ✅ Show loading state during checkout

### **Order Confirmation:**
- ✅ Display order number prominently
- ✅ Show order summary
- ✅ Provide "Track Order" link
- ✅ Show estimated delivery (if available)

---

## 🚨 Error Handling

### **Common Errors:**

1. **Missing Documents (400)**
   - Show which products need which documents
   - Link back to cart to upload documents

2. **Empty Cart (400)**
   - Redirect to products page
   - Show "Add items to cart" message

3. **Validation Errors (400)**
   - Show field-level errors
   - Highlight invalid fields

4. **Network Errors**
   - Show retry button
   - Save form data locally (optional)

---

## ✅ Summary

**After Cart, Frontend Must:**

1. ✅ **Check** if each item needs documents (by category)
2. ✅ **Show** document upload UI for stamp products
3. ✅ **Upload** required documents (Emirates ID, Trade License)
4. ✅ **Validate** all documents uploaded before checkout
5. ✅ **Show** checkout form (billing + shipping)
6. ✅ **Submit** checkout with customer information
7. ✅ **Handle** success → Show order confirmation
8. ✅ **Handle** errors → Show missing documents or validation errors
9. ✅ **Redirect** to orders page after successful checkout

**Key Endpoints:**
- `GET /api/v1/cart/` - Get cart
- `GET /api/v1/cart/items/{id}/requirements/` - Check requirements
- `POST /api/v1/cart/items/{id}/documents/bulk/` - Upload documents
- `POST /api/v1/orders/checkout/` - Create order
- `GET /api/v1/orders/{id}/` - Get order details
- `GET /api/v1/orders/` - List orders

