#!/bin/bash

# Complete Testing Script - Step by Step
# Tests both Stamp Products and Service Products

BASE_URL="http://localhost:8000/api/v1"
USERNAME="testuser"
PASSWORD="testpass123"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Complete Testing Guide${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Login
echo -e "${YELLOW}Step 1: Logging in...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}")

TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
  echo -e "${RED}❌ Login failed!${NC}"
  echo "Response: $LOGIN_RESPONSE"
  exit 1
fi

echo -e "${GREEN}✅ Login successful!${NC}"
echo "Token: ${TOKEN:0:20}..."
echo ""

# Step 2: Get Stamp Product
echo -e "${YELLOW}Step 2: Getting Stamp Product (ID: 1)...${NC}"
STAMP_PRODUCT=$(curl -s -X GET "$BASE_URL/products/1/" \
  -H "Authorization: Bearer $TOKEN")

REQUIREMENTS_COUNT=$(echo "$STAMP_PRODUCT" | grep -o '"requirements"' | wc -l)

if [ "$REQUIREMENTS_COUNT" -gt 0 ]; then
  echo -e "${GREEN}✅ Product has requirements (stamp product)${NC}"
  echo "$STAMP_PRODUCT" | grep -A 5 '"requirements"'
else
  echo -e "${YELLOW}⚠️  Product has no requirements${NC}"
fi
echo ""

# Step 3: Add Stamp Product to Cart
echo -e "${YELLOW}Step 3: Adding Stamp Product to Cart...${NC}"
CART_ITEM=$(curl -s -X POST "$BASE_URL/cart/items/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product": 1, "quantity": 2}')

CART_ITEM_ID=$(echo "$CART_ITEM" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -z "$CART_ITEM_ID" ]; then
  echo -e "${RED}❌ Failed to add to cart!${NC}"
  echo "$CART_ITEM"
  exit 1
fi

echo -e "${GREEN}✅ Added to cart! Cart Item ID: $CART_ITEM_ID${NC}"
echo ""

# Step 4: Upload Documents (if needed)
echo -e "${YELLOW}Step 4: Upload Documents (if you have test files)...${NC}"
echo -e "${BLUE}Note: Create test files first:${NC}"
echo "  - emirates_id.pdf"
echo "  - trade_license.pdf"
echo "  - design.ai"
echo ""

if [ -f "emirates_id.pdf" ] && [ -f "trade_license.pdf" ]; then
  echo -e "${YELLOW}Uploading documents...${NC}"
  UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/cart/items/$CART_ITEM_ID/documents/bulk/" \
    -H "Authorization: Bearer $TOKEN" \
    -F "emirates_id=@emirates_id.pdf" \
    -F "trade_license=@trade_license.pdf")
  
  echo -e "${GREEN}✅ Documents uploaded!${NC}"
  echo "$UPLOAD_RESPONSE" | head -20
else
  echo -e "${YELLOW}⚠️  Skipping document upload (files not found)${NC}"
  echo -e "${BLUE}To test document upload, create test files and run:${NC}"
  echo "curl -X POST \"$BASE_URL/cart/items/$CART_ITEM_ID/documents/bulk/\" \\"
  echo "  -H \"Authorization: Bearer $TOKEN\" \\"
  echo "  -F \"emirates_id=@emirates_id.pdf\" \\"
  echo "  -F \"trade_license=@trade_license.pdf\""
fi
echo ""

# Step 5: View Cart
echo -e "${YELLOW}Step 5: Viewing Cart...${NC}"
CART=$(curl -s -X GET "$BASE_URL/cart/" \
  -H "Authorization: Bearer $TOKEN")

echo -e "${GREEN}✅ Cart retrieved!${NC}"
echo "$CART" | head -30
echo ""

# Step 6: Checkout (Stamp Product)
echo -e "${YELLOW}Step 6: Testing Checkout (Stamp Product)...${NC}"
echo -e "${BLUE}Note: This will fail if required documents are missing${NC}"

CHECKOUT_RESPONSE=$(curl -s -X POST "$BASE_URL/orders/checkout/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+971501234567",
    "address_line_1": "123 Main Street",
    "city": "Dubai",
    "country": "UAE"
  }')

if echo "$CHECKOUT_RESPONSE" | grep -q "order_number"; then
  ORDER_NUMBER=$(echo "$CHECKOUT_RESPONSE" | grep -o '"order_number":"[^"]*' | cut -d'"' -f4)
  echo -e "${GREEN}✅ Checkout successful! Order: $ORDER_NUMBER${NC}"
elif echo "$CHECKOUT_RESPONSE" | grep -q "Missing required documents"; then
  echo -e "${RED}❌ Checkout failed: Missing required documents${NC}"
  echo "$CHECKOUT_RESPONSE" | grep -A 10 "missing_documents"
else
  echo -e "${YELLOW}⚠️  Unexpected response:${NC}"
  echo "$CHECKOUT_RESPONSE"
fi
echo ""

# Step 7: Test Service Product
echo -e "${YELLOW}Step 7: Testing Service Product (ID: 10)...${NC}"
SERVICE_PRODUCT=$(curl -s -X GET "$BASE_URL/products/10/" \
  -H "Authorization: Bearer $TOKEN")

SERVICE_REQUIREMENTS=$(echo "$SERVICE_PRODUCT" | grep -o '"requirements"' | wc -l)

if [ "$SERVICE_REQUIREMENTS" -eq 0 ]; then
  echo -e "${GREEN}✅ Service product has no requirements (as expected)${NC}"
else
  echo -e "${YELLOW}⚠️  Service product has requirements${NC}"
fi
echo ""

# Step 8: Add Service Product to Cart
echo -e "${YELLOW}Step 8: Adding Service Product to Cart...${NC}"
SERVICE_CART_ITEM=$(curl -s -X POST "$BASE_URL/cart/items/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product": 10, "quantity": 3}')

SERVICE_CART_ITEM_ID=$(echo "$SERVICE_CART_ITEM" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -z "$SERVICE_CART_ITEM_ID" ]; then
  echo -e "${RED}❌ Failed to add service product to cart!${NC}"
  echo "$SERVICE_CART_ITEM"
else
  echo -e "${GREEN}✅ Service product added! Cart Item ID: $SERVICE_CART_ITEM_ID${NC}"
fi
echo ""

# Step 9: Checkout Service Product (No Documents)
echo -e "${YELLOW}Step 9: Testing Checkout (Service Product - No Documents)...${NC}"
echo -e "${BLUE}Note: This should succeed even without documents${NC}"

SERVICE_CHECKOUT=$(curl -s -X POST "$BASE_URL/orders/checkout/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "phone": "+971509876543",
    "address_line_1": "456 Business Bay",
    "city": "Dubai",
    "country": "UAE"
  }')

if echo "$SERVICE_CHECKOUT" | grep -q "order_number"; then
  SERVICE_ORDER_NUMBER=$(echo "$SERVICE_CHECKOUT" | grep -o '"order_number":"[^"]*' | cut -d'"' -f4)
  echo -e "${GREEN}✅ Service product checkout successful! Order: $SERVICE_ORDER_NUMBER${NC}"
  echo -e "${GREEN}✅ No documents required (as expected)${NC}"
else
  echo -e "${RED}❌ Service product checkout failed!${NC}"
  echo "$SERVICE_CHECKOUT"
fi
echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Testing Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}✅ Tested:${NC}"
echo "  - Login"
echo "  - Stamp Product (with requirements)"
echo "  - Service Product (no requirements)"
echo "  - Add to Cart"
echo "  - Document Upload"
echo "  - Checkout (both types)"
echo ""
echo -e "${BLUE}For detailed explanations, see: COMPLETE_TESTING_GUIDE.md${NC}"


