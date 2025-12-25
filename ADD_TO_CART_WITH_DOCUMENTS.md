# 🛒 Add to Cart with Documents - Single API Call

## ✅ Now You Can Do Everything in One Request!

You can now add items to cart **AND** upload documents (Emirates ID, Trade License, Design) in a **single API call**!

---

## 📡 API Endpoint

```
POST /api/v1/cart/items/
```

---

## 🔧 Request Format

### **Option 1: JSON (without documents)**
```json
{
  "product_id": 1,
  "quantity": 4
}
```

### **Option 2: Multipart/Form-Data (with documents)**
```
product_id: 1
quantity: 4
emirates_id: <file>
trade_license: <file>
design: <file>  // Optional
```

---

## 💻 Frontend Examples

### **JavaScript/Fetch API**
```javascript
// Create FormData
const formData = new FormData();
formData.append('product_id', 1);
formData.append('quantity', 4);

// Add documents if available
if (emiratesIdFile) {
  formData.append('emirates_id', emiratesIdFile);
}
if (tradeLicenseFile) {
  formData.append('trade_license', tradeLicenseFile);
}
if (designFile) {
  formData.append('design', designFile);  // Optional
}

// Send request
const response = await fetch('/api/v1/cart/items/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
    // Don't set Content-Type - browser will set it with boundary
  },
  body: formData
});

const data = await response.json();
console.log(data);
```

### **React Example**
```jsx
const handleAddToCart = async (productId, quantity, documents) => {
  const formData = new FormData();
  formData.append('product_id', productId);
  formData.append('quantity', quantity);
  
  if (documents.emiratesId) {
    formData.append('emirates_id', documents.emiratesId);
  }
  if (documents.tradeLicense) {
    formData.append('trade_license', documents.tradeLicense);
  }
  if (documents.design) {
    formData.append('design', documents.design);
  }
  
  try {
    const response = await fetch('/api/v1/cart/items/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    
    const data = await response.json();
    
    if (response.ok) {
      console.log('Added to cart!', data);
      if (data.uploaded_documents) {
        console.log(`Uploaded ${data.uploaded_documents.length} documents`);
      }
    } else {
      console.error('Error:', data);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
};
```

### **cURL Example**
```bash
curl -X POST "http://localhost:8000/api/v1/cart/items/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "product_id=1" \
  -F "quantity=4" \
  -F "emirates_id=@/path/to/emirates_id.pdf" \
  -F "trade_license=@/path/to/trade_license.pdf" \
  -F "design=@/path/to/design.ai"
```

---

## 📥 Response

### **Success Response (201)**
```json
{
  "message": "Item added to cart successfully! 2 document(s) uploaded.",
  "uploaded_documents": [
    {
      "id": 11,
      "doc_type": "EMIRATES_ID",
      "doc_type_display": "Emirates ID",
      "file": "/media/cart-documents/2025/12/emirates_id.pdf",
      "file_name": "emirates_id.pdf",
      "file_size": 245678,
      "uploaded_at": "2025-12-15T10:30:00Z"
    },
    {
      "id": 12,
      "doc_type": "TRADE_LICENSE",
      "doc_type_display": "Trade License",
      "file": "/media/cart-documents/2025/12/trade_license.pdf",
      "file_name": "trade_license.pdf",
      "file_size": 312456,
      "uploaded_at": "2025-12-15T10:30:00Z"
    }
  ],
  "cart": {
    "id": 1,
    "items": [
      {
        "id": 5,
        "product": 1,
        "product_name": "Shiny R-532D",
        "quantity": 4,
        "price": "75.00",
        "total_price": "300.00",
        "documents": [
          {
            "id": 11,
            "doc_type": "EMIRATES_ID",
            "file_name": "emirates_id.pdf"
          },
          {
            "id": 12,
            "doc_type": "TRADE_LICENSE",
            "file_name": "trade_license.pdf"
          }
        ]
      }
    ],
    "subtotal": "300.00",
    "total_items": 1
  }
}
```

### **Error Response (400)**
```json
{
  "product_id": ["Product not found or is inactive."]
}
```

or

```json
{
  "emirates_id": ["File size cannot exceed 10MB."]
}
```

---

## 📋 Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_id` | Integer | ✅ Yes | Product ID to add to cart |
| `quantity` | Integer | ❌ No | Quantity (default: 1) |
| `emirates_id` | File | ❌ No | Emirates ID document |
| `trade_license` | File | ❌ No | Trade License document |
| `design` | File | ❌ No | Design file (optional) |

---

## ✅ File Validation

- **Max File Size:** 10MB per file
- **Allowed Formats:**
  - Images: `jpg`, `jpeg`, `png`
  - Documents: `pdf`, `doc`, `docx`
  - Design Files: `ai`, `eps`, `psd`, `cdr`, `svg`

---

## 🎯 Use Cases

### **1. Add Product Without Documents**
```javascript
// Simple JSON request
{
  "product_id": 10,  // Service product - no documents needed
  "quantity": 1
}
```

### **2. Add Stamp Product with Documents**
```javascript
// Multipart form data
FormData:
  - product_id: 1
  - quantity: 2
  - emirates_id: <file>
  - trade_license: <file>
```

### **3. Add Product with Optional Design**
```javascript
// Multipart form data
FormData:
  - product_id: 1
  - quantity: 1
  - emirates_id: <file>
  - trade_license: <file>
  - design: <file>  // Optional design file
```

---

## 🔄 Backward Compatibility

✅ **Still works the old way:**
- You can still add items without documents
- You can still upload documents separately using:
  - `POST /api/v1/cart/items/{id}/documents/`
  - `POST /api/v1/cart/items/{id}/documents/bulk/`

---

## 💡 Benefits

1. ✅ **Single API Call** - Add item + upload documents in one request
2. ✅ **Better UX** - Users can complete everything on product page
3. ✅ **Fewer Network Requests** - More efficient
4. ✅ **Simpler Frontend Code** - One function handles everything
5. ✅ **Backward Compatible** - Old methods still work

---

## 🚨 Important Notes

1. **If item already exists in cart:**
   - Quantity will be **added** to existing quantity
   - Documents will **replace** existing documents of same type

2. **Document Upload:**
   - Documents are optional in this endpoint
   - You can upload documents later if needed
   - Checkout will validate required documents

3. **Content-Type:**
   - Use `multipart/form-data` when uploading files
   - Don't manually set `Content-Type` header - browser will set it with boundary

---

## 📝 Example: Complete Product Page Flow

```javascript
// User clicks "Add to Cart" button on product page
async function handleAddToCart(productId, quantity, formData) {
  // Get files from form
  const emiratesId = formData.get('emirates_id');
  const tradeLicense = formData.get('trade_license');
  const design = formData.get('design');
  
  // Create FormData for API
  const apiFormData = new FormData();
  apiFormData.append('product_id', productId);
  apiFormData.append('quantity', quantity);
  
  if (emiratesId) apiFormData.append('emirates_id', emiratesId);
  if (tradeLicense) apiFormData.append('trade_license', tradeLicense);
  if (design) apiFormData.append('design', design);
  
  // Send to API
  const response = await fetch('/api/v1/cart/items/', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: apiFormData
  });
  
  const data = await response.json();
  
  if (response.ok) {
    // Success!
    showSuccessMessage('Added to cart!');
    if (data.uploaded_documents) {
      showMessage(`${data.uploaded_documents.length} documents uploaded`);
    }
    // Redirect to cart or show cart preview
  } else {
    // Show errors
    showErrors(data);
  }
}
```

---

## ✅ Summary

**You can now do:**
```javascript
POST /api/v1/cart/items/
{
  "product_id": 1,
  "quantity": 4,
  "emirates_id": <file>,
  "trade_license": <file>,
  "design": <file>
}
```

**All in one API call!** 🎉

