# 🛒 Order & Checkout Guide

## Complete Flow: Cart → Checkout → Order

After items are in your cart (with documents uploaded), here's what to do for orders:

---

## 📋 Step-by-Step Order Flow

### **Step 1: Verify Cart & Documents** ✅

Before checkout, make sure:
- ✅ Cart has items
- ✅ All required documents are uploaded (for stamp products)

**Check Cart:**
```javascript
GET /api/v1/cart/
Authorization: Bearer {token}
```

**Check Requirements for Each Item:**
```javascript
GET /api/v1/cart/items/{item_id}/requirements/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "cart_item_id": 5,
  "all_required_uploaded": true,  // ← Must be true!
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

### **Step 2: Show Checkout Form** 📝

Display a checkout form with:

**Required Fields:**
- First Name
- Last Name
- Email
- Phone
- Address Line 1
- City
- Country

**Optional Fields:**
- Company Name
- Address Line 2
- State
- Postal Code
- Order Notes

---

### **Step 3: Submit Checkout** 🚀

**API Endpoint:**
```
POST /api/v1/orders/checkout/
```

**Note:** Authentication is **NOT required** for checkout! Works for both:
- ✅ **Guest users** (no token) - Uses session_id to find cart
- ✅ **Authenticated users** (with token) - Uses user to find cart

**Request:**
```javascript
POST /api/v1/orders/checkout/
// Authorization: Bearer {token}  // Optional - only if user is authenticated
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

**JavaScript Example (Works for Both Guest and Authenticated):**
```javascript
async function checkout(customerData, token = null) {
  const headers = {
    'Content-Type': 'application/json'
  };
  
  // Add token only if user is authenticated (optional)
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch('/api/v1/orders/checkout/', {
    method: 'POST',
    headers: headers,
    credentials: 'include',  // Important: Include session cookie for guest users
    body: JSON.stringify({
      first_name: customerData.firstName,
      last_name: customerData.lastName,
      email: customerData.email,
      phone: customerData.phone,
      company_name: customerData.companyName || '',
      address_line_1: customerData.address1,
      address_line_2: customerData.address2 || '',
      city: customerData.city,
      state: customerData.state || '',
      country: customerData.country,
      postal_code: customerData.postalCode || '',
      order_notes: customerData.notes || ''
    })
  });
  
  return await response.json();
}
```

---

### **Step 4: Handle Checkout Response** 📥

#### **✅ Success Response (201 Created)**

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
  "total": "300.00",
  "subtotal": "300.00",
  "shipping_cost": "0.00",
  "tax": "0.00",
  "items": [
    {
      "id": 1,
      "product": 1,
      "product_name": "Shiny R-532D",
      "quantity": 4,
      "price": "75.00",
      "total": "300.00"
    }
  ],
  "documents": [
    {
      "id": 1,
      "doc_type": "EMIRATES_ID",
      "file": "/media/orders/2025/12/emirates_id.pdf",
      "file_name": "emirates_id.pdf",
      "file_size": 245678
    },
    {
      "id": 2,
      "doc_type": "TRADE_LICENSE",
      "file": "/media/orders/2025/12/trade_license.pdf",
      "file_name": "trade_license.pdf",
      "file_size": 312456
    }
  ],
  "created_at": "2025-12-15T10:30:00Z"
}
```

**What Happens:**
- ✅ Order is created
- ✅ All cart items are converted to order items
- ✅ All documents are copied from cart to order
- ✅ Cart is automatically cleared
- ✅ Order number is generated
- ✅ For guests: Order has `user=None`, identified by email
- ✅ For authenticated: Order linked to user account

**Frontend Action:**
```javascript
if (response.status === 201) {
  const order = await response.json();
  
  // Show success message
  showSuccessMessage(`Order ${order.order_number} created successfully!`);
  
  // Redirect to order confirmation page
  router.push(`/orders/${order.id}/confirmation`);
  
  // Or redirect to orders list
  router.push('/orders');
}
```

#### **❌ Error Response - Missing Documents (400)**

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

**Frontend Action:**
```javascript
if (response.status === 400) {
  const error = await response.json();
  
  if (error.error === 'Missing required documents') {
    // Show error message
    showError('Please upload all required documents');
    
    // Highlight missing documents
    error.missing_documents.forEach(missing => {
      highlightProduct(missing.product_id);
      showMissingDocument(missing.missing_document);
    });
    
    // Redirect back to cart
    router.push('/cart');
  }
}
```

#### **❌ Error Response - Empty Cart (400)**

```json
{
  "error": "Cart is empty"
}
```

#### **❌ Error Response - Validation Errors (400)**

```json
{
  "first_name": ["This field is required."],
  "email": ["Enter a valid email address."]
}
```

---

### **Step 5: Order Confirmation Page** 🎉

Display order details:

```javascript
// Get order details
const order = await fetch(`/api/v1/orders/${orderId}/`, {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// Display:
// - Order Number (important for tracking!)
// - Order Status
// - Items ordered
// - Total amount
// - Shipping address
// - Documents uploaded
// - Created date
```

**UI Elements:**
- ✅ Success message
- ✅ Order number (prominently displayed)
- ✅ Order summary
- ✅ "View Orders" button
- ✅ "Track Order" link (if available)

---

### **Step 6: View Orders** 📋

**List All Orders:**
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
      "total": "300.00",
      "items_count": 1,
      "created_at": "2025-12-15T10:30:00Z"
    },
    {
      "id": 2,
      "order_number": "ORD-2025-002",
      "full_name": "John Doe",
      "email": "john@example.com",
      "status": "confirmed",
      "payment_status": "paid",
      "total": "150.00",
      "items_count": 1,
      "created_at": "2025-12-14T09:15:00Z"
    }
  ]
}
```

**Get Single Order Details:**
```javascript
GET /api/v1/orders/{order_id}/
Authorization: Bearer {token}
```

---

## 🔄 Complete Flow Diagram

```
┌─────────────────┐
│   Cart Ready    │
│  (with items &  │
│   documents)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Show Checkout Form      │
│ (Billing + Shipping)    │
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
         │      ├─ Cart Cleared
         │      ├─ Documents Copied
         │      └─ Order Number Generated
         │          │
         │          ▼
         │  ┌─────────────────────┐
         │  │ Order Confirmation  │
         │  │ Show Order Details  │
         │  └─────────────────────┘
         │
         └─ Error (400)
            ├─ Missing Documents
            │  └─► Show Error
            │      └─► Go Back to Cart
            │
            ├─ Empty Cart
            │  └─► Show Error
            │
            └─ Validation Errors
               └─► Show Field Errors
```

---

## 💻 Complete Frontend Example

```javascript
// Complete checkout flow
class CheckoutService {
  constructor(token) {
    this.token = token;
    this.baseUrl = '/api/v1';
  }
  
  // Step 1: Validate cart before checkout
  async validateCart() {
    const cartResponse = await fetch(`${this.baseUrl}/cart/`, {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
    const cart = await cartResponse.json();
    
    if (!cart.items || cart.items.length === 0) {
      throw new Error('Cart is empty');
    }
    
    // Check requirements for each item
    const validationErrors = [];
    for (const item of cart.items) {
      const reqResponse = await fetch(
        `${this.baseUrl}/cart/items/${item.id}/requirements/`,
        { headers: { 'Authorization': `Bearer ${this.token}` } }
      );
      const reqData = await reqResponse.json();
      
      if (!reqData.all_required_uploaded) {
        const missing = reqData.requirements
          .filter(r => r.is_required && !r.is_uploaded)
          .map(r => r.doc_type_display);
        
        validationErrors.push({
          product: item.product_name,
          missing: missing
        });
      }
    }
    
    if (validationErrors.length > 0) {
      throw {
        type: 'MISSING_DOCUMENTS',
        errors: validationErrors
      };
    }
    
    return cart;
  }
  
  // Step 2: Submit checkout
  async checkout(customerData) {
    try {
      // Validate cart first
      await this.validateCart();
      
      // Submit checkout
      const response = await fetch(`${this.baseUrl}/orders/checkout/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          first_name: customerData.firstName,
          last_name: customerData.lastName,
          email: customerData.email,
          phone: customerData.phone,
          company_name: customerData.companyName || '',
          address_line_1: customerData.address1,
          address_line_2: customerData.address2 || '',
          city: customerData.city,
          state: customerData.state || '',
          country: customerData.country,
          postal_code: customerData.postalCode || '',
          order_notes: customerData.notes || ''
        })
      });
      
      const data = await response.json();
      
      if (response.status === 201) {
        return {
          success: true,
          order: data
        };
      } else if (response.status === 400) {
        if (data.error === 'Missing required documents') {
          return {
            success: false,
            error: 'MISSING_DOCUMENTS',
            missingDocuments: data.missing_documents
          };
        } else {
          return {
            success: false,
            error: 'VALIDATION_ERROR',
            errors: data
          };
        }
      } else {
        return {
          success: false,
          error: 'UNKNOWN_ERROR',
          message: 'An error occurred'
        };
      }
    } catch (error) {
      if (error.type === 'MISSING_DOCUMENTS') {
        return {
          success: false,
          error: 'MISSING_DOCUMENTS',
          errors: error.errors
        };
      }
      throw error;
    }
  }
  
  // Step 3: Get order details
  async getOrder(orderId) {
    const response = await fetch(`${this.baseUrl}/orders/${orderId}/`, {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
    return await response.json();
  }
  
  // Step 4: List all orders
  async listOrders() {
    const response = await fetch(`${this.baseUrl}/orders/`, {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
    return await response.json();
  }
}

// Usage
const checkoutService = new CheckoutService(token);

// Handle checkout form submission
async function handleCheckoutSubmit(formData) {
  const result = await checkoutService.checkout(formData);
  
  if (result.success) {
    // Success! Redirect to confirmation
    router.push(`/orders/${result.order.id}/confirmation`);
  } else if (result.error === 'MISSING_DOCUMENTS') {
    // Show missing documents error
    showMissingDocumentsError(result.missingDocuments);
    router.push('/cart');
  } else if (result.error === 'VALIDATION_ERROR') {
    // Show validation errors
    showValidationErrors(result.errors);
  }
}
```

---

## 📱 React Component Example

```jsx
function CheckoutForm() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address1: '',
    city: '',
    country: 'UAE'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/v1/orders/checkout/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          first_name: formData.firstName,
          last_name: formData.lastName,
          email: formData.email,
          phone: formData.phone,
          address_line_1: formData.address1,
          city: formData.city,
          country: formData.country
        })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        // Success!
        router.push(`/orders/${data.id}/confirmation`);
      } else {
        // Handle errors
        if (data.error === 'Missing required documents') {
          setError('Please upload all required documents');
        } else {
          setError('Please check your information');
        }
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <input
        value={formData.firstName}
        onChange={(e) => setFormData({...formData, firstName: e.target.value})}
        placeholder="First Name"
        required
      />
      {/* ... other fields ... */}
      
      {error && <div className="error">{error}</div>}
      
      <button type="submit" disabled={loading}>
        {loading ? 'Processing...' : 'Place Order'}
      </button>
    </form>
  );
}
```

---

## ✅ Summary

**For Orders, You Need To:**

1. ✅ **Validate Cart** - Check items and documents are ready
2. ✅ **Show Checkout Form** - Collect customer information
3. ✅ **Submit Checkout** - `POST /api/v1/orders/checkout/` with customer data
4. ✅ **Handle Response**:
   - Success → Show order confirmation
   - Missing Documents → Show error, go back to cart
   - Validation Errors → Show field errors
5. ✅ **Display Order** - Show order details and order number
6. ✅ **List Orders** - `GET /api/v1/orders/` to show all orders

**Key Endpoints:**
- `POST /api/v1/orders/checkout/` - Create order from cart (✅ No auth required!)
- `GET /api/v1/orders/` - List all orders (⚠️ Auth required - only for authenticated users)
- `GET /api/v1/orders/{id}/` - Get order details (⚠️ Auth required - only for authenticated users)

**What Backend Does Automatically:**
- ✅ Validates required documents
- ✅ Finds cart (by user if authenticated, by session_id if guest)
- ✅ Creates order from cart
- ✅ Copies all documents from cart to order
- ✅ Clears cart after successful order
- ✅ Generates order number
- ✅ Links order to user (if authenticated) or sets user=None (for guests)

