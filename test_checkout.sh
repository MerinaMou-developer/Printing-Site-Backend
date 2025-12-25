#!/bin/bash

# Test Checkout and Orders API
# Usage: ./test_checkout.sh

BASE_URL="http://localhost:8000/api/v1"
USERNAME="testuser"
PASSWORD="testpass123"

echo "🧪 Testing Checkout and Orders API"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Login
echo "Step 1: Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}")

TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
  echo -e "${RED}❌ Login failed!${NC}"
  echo "Response: $LOGIN_RESPONSE"
  exit 1
fi

echo -e "${GREEN}✅ Logged in successfully${NC}"
echo "Token: ${TOKEN:0:30}..."
echo ""

# Step 2: Get Cart
echo "Step 2: Getting cart..."
CART_RESPONSE=$(curl -s -X GET "$BASE_URL/cart/" \
  -H "Authorization: Bearer $TOKEN")

CART_ITEMS=$(echo "$CART_RESPONSE" | grep -o '"items":\[[^]]*\]' | wc -l)

if [ "$CART_ITEMS" -eq 0 ]; then
  echo -e "${YELLOW}⚠️  Cart is empty. Adding item...${NC}"
  
  # Add item to cart
  ADD_RESPONSE=$(curl -s -X POST "$BASE_URL/cart/items/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"product_id": 1, "quantity": 2, "price": "75.00"}')
  
  echo "$ADD_RESPONSE" | grep -q "successfully" && echo -e "${GREEN}✅ Item added to cart${NC}" || echo -e "${RED}❌ Failed to add item${NC}"
else
  echo -e "${GREEN}✅ Cart has items${NC}"
fi
echo ""

# Step 3: Check Requirements
echo "Step 3: Checking document requirements..."
# Get first cart item ID (simplified - in real scenario, parse JSON properly)
echo -e "${YELLOW}⚠️  Note: Make sure all required documents are uploaded!${NC}"
echo ""

# Step 4: Test Checkout
echo "Step 4: Testing checkout..."
CHECKOUT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/orders/checkout/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+971501234567",
    "address_line_1": "123 Main Street",
    "city": "Dubai",
    "country": "United Arab Emirates"
  }')

HTTP_CODE=$(echo "$CHECKOUT_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$CHECKOUT_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "201" ]; then
  echo -e "${GREEN}✅ Checkout successful!${NC}"
  ORDER_ID=$(echo "$RESPONSE_BODY" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
  ORDER_NUMBER=$(echo "$RESPONSE_BODY" | grep -o '"order_number":"[^"]*' | cut -d'"' -f4)
  echo "Order ID: $ORDER_ID"
  echo "Order Number: $ORDER_NUMBER"
elif [ "$HTTP_CODE" == "400" ]; then
  echo -e "${RED}❌ Checkout failed: Bad Request${NC}"
  echo "$RESPONSE_BODY" | grep -o '"error":"[^"]*' | cut -d'"' -f4
  echo "$RESPONSE_BODY"
else
  echo -e "${RED}❌ Checkout failed with HTTP $HTTP_CODE${NC}"
  echo "$RESPONSE_BODY"
fi
echo ""

# Step 5: List Orders
echo "Step 5: Listing orders..."
ORDERS_RESPONSE=$(curl -s -X GET "$BASE_URL/orders/" \
  -H "Authorization: Bearer $TOKEN")

ORDER_COUNT=$(echo "$ORDERS_RESPONSE" | grep -o '"count":[0-9]*' | cut -d':' -f2)
echo -e "${GREEN}✅ Found $ORDER_COUNT order(s)${NC}"
echo ""

# Step 6: Get Order Details (if order was created)
if [ ! -z "$ORDER_ID" ]; then
  echo "Step 6: Getting order details..."
  ORDER_DETAILS=$(curl -s -X GET "$BASE_URL/orders/$ORDER_ID/" \
    -H "Authorization: Bearer $TOKEN")
  
  ORDER_STATUS=$(echo "$ORDER_DETAILS" | grep -o '"status":"[^"]*' | cut -d'"' -f4)
  ORDER_TOTAL=$(echo "$ORDER_DETAILS" | grep -o '"total":"[^"]*' | cut -d'"' -f4)
  
  echo -e "${GREEN}✅ Order Details:${NC}"
  echo "Status: $ORDER_STATUS"
  echo "Total: $ORDER_TOTAL"
  echo ""
fi

echo "===================================="
echo -e "${GREEN}✅ Test completed!${NC}"
echo ""
echo "Next steps:"
echo "1. Upload required documents to cart items"
echo "2. Try checkout again"
echo "3. (Admin) Update order status to 'delivered'"
echo "4. Verify product total_sold count is updated"

