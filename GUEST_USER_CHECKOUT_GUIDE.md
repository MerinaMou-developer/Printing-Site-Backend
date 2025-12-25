# 👤 Guest User Checkout - Complete Guide

## 🎯 For Guest Users (No Authentication Required)

This guide shows you how to complete checkout as a guest user, including uploading documents.

---

## 📋 Complete Flow for Guest Users

### **Step 1: Add Items to Cart (with documents)**

**Important:** For guest users, you need to enable **session cookies** in your client (Postman, browser, etc.)

**API Call:**
```http
POST /api/v1/cart/items/
Content-Type: multipart/form-data
```

**Request Body (multipart/form-data):**
```
product_id: 2
quantity: 1
emirates_id: <file>
trade_license: <file>
design: <file>  // Optional
```

**cURL Example:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/cart/items/" \
  -b cookies.txt \
  -c cookies.txt \
  -F "product_id=2" \
  -F "quantity=1" \
  -F "emirates_id=@/path/to/emirates_id.pdf" \
  -F "trade_license=@/path/to/trade_license.pdf"
```

**Response:**
```json
{
  "message": "Item added to cart successfully! 2 document(s) uploaded.",
  "uploaded_documents": [
    {
      "id": 1,
      "doc_type": "EMIRATES_ID",
      "file_name": "emirates_id.pdf"
    },
    {
      "id": 2,
      "doc_type": "TRADE_LICENSE",
      "file_name": "trade_license.pdf"
    }
  ],
  "cart": {
    "id": 1,
    "items": [
      {
        "id": 1,
        "product": 2,
        "product_name": "R-532D",
        "quantity": 1,
        "documents": [...]
      }
    ]
  }
}
```

---

### **Step 2: Verify Cart & Documents**

**Check Cart:**
```http
GET /api/v1/cart/
```

**Check Requirements:**
```http
GET /api/v1/cart/items/{item_id}/requirements/
```

**Response:**
```json
{
  "cart_item_id": 1,
  "product_id": 2,
  "product_name": "R-532D",
  "all_required_uploaded": true,  // ✅ Must be true!
  "requirements": [
    {
      "doc_type": "EMIRATES_ID",
      "is_required": true,
      "is_uploaded": true  // ✅ Uploaded
    },
    {
      "doc_type": "TRADE_LICENSE",
      "is_required": true,
      "is_uploaded": true  // ✅ Uploaded
    }
  ]
}
```

---

### **Step 3: Checkout**

**API Call:**
```http
POST /api/v1/orders/checkout/
Content-Type: application/json
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+971501234567",
  "company_name": "My Company",
  "address_line_1": "123 Main Street",
  "address_line_2": "Building 5",
  "city": "Dubai",
  "state": "Dubai",
  "country": "UAE",
  "postal_code": "12345",
  "order_notes": "Please deliver before 5 PM"
}
```

**Response (Success):**
```json
{
  "id": 1,
  "order_number": "ORD-2025-001",
  "status": "pending",
  "payment_status": "pending",
  "user": null,  // ← Guest order
  "email": "john@example.com",
  "total": "75.00",
  "items": [...],
  "documents": [...]
}
```

---

## 🔧 Postman Setup for Guest Users

### **Important: Enable Session Cookies!**

**Problem:** Postman doesn't automatically handle Django sessions. You need to:

### **Option 1: Use Postman's Cookie Manager**

1. **Enable Cookies:**
   - Go to Postman Settings → General
   - Enable "Automatically follow redirects"
   - Enable "Send cookies"

2. **First Request (Add to Cart):**
   - Make a request to `GET /api/v1/cart/` or `POST /api/v1/cart/items/`
   - Postman will automatically save the session cookie

3. **Subsequent Requests:**
   - Postman will automatically send the session cookie
   - All requests will use the same session

### **Option 2: Manual Cookie Management**

1. **Get Session Cookie:**
   ```http
   GET /api/v1/cart/
   ```
   - Check Response Headers → `Set-Cookie: sessionid=...`
   - Copy the `sessionid` value

2. **Add Cookie to All Requests:**
   - In Postman, go to Headers
   - Add: `Cookie: sessionid=YOUR_SESSION_ID`

### **Option 3: Use Postman Environment Variables**

1. **Create Environment Variable:**
   - Variable: `sessionid`
   - Initial Value: (empty)

2. **In Tests Tab (for first request):**
   ```javascript
   // Extract session cookie
   const cookies = pm.response.headers.get("Set-Cookie");
   if (cookies) {
       const sessionMatch = cookies.match(/sessionid=([^;]+)/);
       if (sessionMatch) {
           pm.environment.set("sessionid", sessionMatch[1]);
       }
   }
   ```

3. **In Headers (for all requests):**
   ```
   Cookie: sessionid={{sessionid}}
   ```

---

## 📝 Postman Step-by-Step for Guest Checkout

### **Step 1: Add Item to Cart with Documents**

**Request:**
```
POST http://127.0.0.1:8000/api/v1/cart/items/
```

**Headers:**
```
Content-Type: multipart/form-data
```

**Body (form-data):**
| Key | Type | Value |
|-----|------|-------|
| product_id | Text | 2 |
| quantity | Text | 1 |
| emirates_id | File | [Select File] |
| trade_license | File | [Select File] |

**Important:** 
- Make sure cookies are enabled
- Postman will save session cookie automatically

**Response:**
```json
{
  "message": "Item added to cart successfully! 2 document(s) uploaded.",
  "cart": {
    "items": [
      {
        "id": 1,
        "product_name": "R-532D",
        "documents": [...]
      }
    ]
  }
}
```

---

### **Step 2: Verify Documents Uploaded**

**Request:**
```
GET http://127.0.0.1:8000/api/v1/cart/items/1/requirements/
```

**Headers:**
```
Cookie: sessionid=YOUR_SESSION_ID
```

**Response:**
```json
{
  "all_required_uploaded": true  // ✅ Ready for checkout
}
```

---

### **Step 3: Checkout**

**Request:**
```
POST http://127.0.0.1:8000/api/v1/orders/checkout/
```

**Headers:**
```
Content-Type: application/json
Cookie: sessionid=YOUR_SESSION_ID
```

**Body (raw JSON):**
```json
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

**Response (Success):**
```json
{
  "id": 1,
  "order_number": "ORD-2025-001",
  "status": "pending",
  "total": "75.00"
}
```

---

## 🐍 Python Requests Example

```python
import requests

# Base URL
BASE_URL = "http://127.0.0.1:8000/api/v1"

# Create session to maintain cookies
session = requests.Session()

# Step 1: Add item to cart with documents
files = {
    'emirates_id': open('emirates_id.pdf', 'rb'),
    'trade_license': open('trade_license.pdf', 'rb')
}
data = {
    'product_id': 2,
    'quantity': 1
}

response = session.post(
    f"{BASE_URL}/cart/items/",
    files=files,
    data=data
)
print("Added to cart:", response.json())

# Step 2: Verify requirements
cart_item_id = response.json()['cart']['items'][0]['id']
req_response = session.get(
    f"{BASE_URL}/cart/items/{cart_item_id}/requirements/"
)
print("Requirements:", req_response.json())

# Step 3: Checkout
checkout_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+971501234567",
    "address_line_1": "123 Main Street",
    "city": "Dubai",
    "country": "UAE"
}

order_response = session.post(
    f"{BASE_URL}/orders/checkout/",
    json=checkout_data
)
print("Order created:", order_response.json())
```

---

## 🌐 JavaScript/Fetch Example

```javascript
// Guest checkout flow
async function guestCheckout() {
  // Step 1: Add item to cart with documents
  const formData = new FormData();
  formData.append('product_id', 2);
  formData.append('quantity', 1);
  formData.append('emirates_id', emiratesIdFile);
  formData.append('trade_license', tradeLicenseFile);
  
  const cartResponse = await fetch('/api/v1/cart/items/', {
    method: 'POST',
    credentials: 'include',  // Important: Include cookies!
    body: formData
  });
  
  const cartData = await cartResponse.json();
  console.log('Added to cart:', cartData);
  
  // Step 2: Verify requirements
  const cartItemId = cartData.cart.items[0].id;
  const reqResponse = await fetch(
    `/api/v1/cart/items/${cartItemId}/requirements/`,
    { credentials: 'include' }
  );
  const reqData = await reqResponse.json();
  console.log('Requirements:', reqData);
  
  // Step 3: Checkout
  const checkoutResponse = await fetch('/api/v1/orders/checkout/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',  // Important: Include cookies!
    body: JSON.stringify({
      first_name: "John",
      last_name: "Doe",
      email: "john@example.com",
      phone: "+971501234567",
      address_line_1: "123 Main Street",
      city: "Dubai",
      country: "UAE"
    })
  });
  
  const order = await checkoutResponse.json();
  console.log('Order created:', order);
  return order;
}
```

---

## ⚠️ Common Issues & Solutions

### **Issue 1: "Cart not found" Error**

**Problem:** Session cookie not being sent

**Solution:**
- ✅ Enable cookies in Postman settings
- ✅ Use `credentials: 'include'` in fetch requests
- ✅ Use `requests.Session()` in Python
- ✅ Manually add `Cookie: sessionid=...` header

### **Issue 2: "Missing required documents" Error**

**Problem:** Documents not uploaded before checkout

**Solution:**
1. Upload documents when adding to cart:
   ```
   POST /api/v1/cart/items/
   - product_id
   - emirates_id (file)
   - trade_license (file)
   ```

2. Or upload documents separately:
   ```
   POST /api/v1/cart/items/{id}/documents/bulk/
   - emirates_id (file)
   - trade_license (file)
   ```

3. Verify before checkout:
   ```
   GET /api/v1/cart/items/{id}/requirements/
   # Check: "all_required_uploaded": true
   ```

### **Issue 3: Session Expires**

**Problem:** Session cookie expires between requests

**Solution:**
- ✅ Make requests within session timeout period
- ✅ Re-add item to cart if session expires
- ✅ Consider increasing session timeout in Django settings

---

## ✅ Quick Checklist for Guest Checkout

- [ ] **Enable cookies/session** in your client
- [ ] **Add item to cart** with required documents
- [ ] **Verify documents uploaded** (check requirements endpoint)
- [ ] **Checkout** with customer information
- [ ] **Save order number** for tracking

---

## 📊 Flow Diagram

```
Guest User Flow:
┌─────────────────────┐
│ 1. Add to Cart      │
│ POST /cart/items/   │
│ + documents         │
│ (Session created)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 2. Verify Cart      │
│ GET /cart/          │
│ (Uses session)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 3. Check Requirements│
│ GET /cart/items/    │
│ {id}/requirements/  │
│ (Uses session)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 4. Checkout         │
│ POST /orders/       │
│ checkout/           │
│ (Uses session)      │
│ (Creates order)     │
└─────────────────────┘
```

---

## 🎯 Key Points for Guest Users

1. ✅ **No Authentication Required** - No token needed
2. ✅ **Session-Based** - Uses browser/Postman session cookie
3. ✅ **Upload Documents First** - Before checkout
4. ✅ **Verify Before Checkout** - Check requirements endpoint
5. ✅ **Order Identified by Email** - Use email + order_number to track

---

## 📞 Need Help?

If you're getting errors:

1. **"Cart not found"** → Check session cookie is being sent
2. **"Missing documents"** → Upload documents before checkout
3. **"Session expired"** → Re-add items to cart

**Test Session:**
```http
GET /api/v1/cart/
# Should return your cart (even if empty)
# If 404, session not working
```

