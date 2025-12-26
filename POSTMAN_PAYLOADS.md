# Postman API Payloads

This document contains JSON payloads for creating categories and products via the API.

---

## Base URL
```
http://localhost:8000/api/v1/
```

**Note:** All POST requests require Admin authentication. Make sure to include your authentication token in the headers:
```
Authorization: Bearer <your_access_token>
Content-Type: application/json
```

---

## 1. Create Categories

**Endpoint:** `POST /api/v1/categories/`

**Note:** Slug is optional - it will be auto-generated from the name if not provided.

---

### Category 1: Dater Stamp Products

```json
{
  "name": "Dater Stamp Products",
  "slug": "dater-stamp-products",
  "description": "Professional dater stamps with date, company name and received text",
  "is_active": true,
  "order": 1
}
```

---

### Category 2: Handy and Pocket Stamps

```json
{
  "name": "Handy and Pocket Stamps",
  "slug": "handy-and-pocket-stamps",
  "description": "Compact stamps for on-the-go use",
  "is_active": true,
  "order": 2
}
```

---

### Category 3: Heavy Duty Stamps

```json
{
  "name": "Heavy Duty Stamps",
  "slug": "heavy-duty-stamps",
  "description": "Heavy-duty professional stamps for high-volume use",
  "is_active": true,
  "order": 3
}
```

---

### Category 4: Oval Self Ink Stamps

```json
{
  "name": "Oval Self Ink Stamps",
  "slug": "oval-self-ink-stamps",
  "description": "Professional oval self-inking stamps in various colors",
  "is_active": true,
  "order": 4
}
```

---

### Category 5: Round Self Ink Stamps

```json
{
  "name": "Round Self Ink Stamps",
  "slug": "round-self-ink-stamps",
  "description": "Professional round self-inking stamps in various colors",
  "is_active": true,
  "order": 5
}
```

---

## 2. Create Products

**Endpoint:** `POST /api/v1/products/`

**Important:** 
- You need to get the category ID first (from the category creation response)
- Replace `"category": 1` with the actual category ID from your database
- At least one of `category` or `service` must be provided
- `price` is required (in AED)
- `description` is required

---

### Products for "Dater Stamp Products" Category (Category ID: Replace with actual ID)

#### Product 1: Shiny R-532D

```json
{
  "name": "Shiny R-532D",
  "slug": "shiny-r-532d",
  "category": 1,
  "description": "Professional dater stamp with date, company name and received text",
  "short_description": "Professional dater stamp with date, company name and received text",
  "price": "150.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 2: Shiny R-538D Blue

```json
{
  "name": "Shiny R-538D Blue",
  "slug": "shiny-r-538d-blue",
  "category": 1,
  "description": "Blue professional dater stamp with date, company name and received text",
  "short_description": "Blue professional dater stamp with date, company name and received text",
  "price": "150.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 3: Shiny R-542D Black

```json
{
  "name": "Shiny R-542D Black",
  "slug": "shiny-r-542d-black",
  "category": 1,
  "description": "Black professional dater stamp with date, company name and received text",
  "short_description": "Black professional dater stamp with date, company name and received text",
  "price": "150.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 4: Shiny R-542D T12 Red

```json
{
  "name": "Shiny R-542D T12 Red",
  "slug": "shiny-r-542d-t12-red",
  "category": 1,
  "description": "Red professional dater stamp with date, company name and received text",
  "short_description": "Red professional dater stamp with date, company name and received text",
  "price": "150.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 5: Shiny R-552D Blue

```json
{
  "name": "Shiny R-552D Blue",
  "slug": "shiny-r-552d-blue",
  "category": 1,
  "description": "Blue professional dater stamp with date, company name and received text",
  "short_description": "Blue professional dater stamp with date, company name and received text",
  "price": "150.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 6: Shiny S-530D

```json
{
  "name": "Shiny S-530D",
  "slug": "shiny-s-530d",
  "category": 1,
  "description": "Professional square dater stamp with date, company name and received text",
  "short_description": "Professional square dater stamp with date, company name and received text",
  "price": "150.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 7: Shiny S-538D

```json
{
  "name": "Shiny S-538D",
  "slug": "shiny-s-538d",
  "category": 1,
  "description": "Professional square dater stamp with date, company name and received text",
  "short_description": "Professional square dater stamp with date, company name and received text",
  "price": "150.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 8: Shiny S-722

```json
{
  "name": "Shiny S-722",
  "slug": "shiny-s-722",
  "category": 1,
  "description": "Professional pocket-sized dater stamp",
  "short_description": "Professional pocket-sized dater stamp",
  "price": "120.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 9: Shiny S-723 Green

```json
{
  "name": "Shiny S-723 Green",
  "slug": "shiny-s-723-green",
  "category": 1,
  "description": "Green professional pocket-sized dater stamp",
  "short_description": "Green professional pocket-sized dater stamp",
  "price": "120.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 10: Shiny S-723 Others

```json
{
  "name": "Shiny S-723 Others",
  "slug": "shiny-s-723-others",
  "category": 1,
  "description": "Professional pocket-sized dater stamp in various colors",
  "short_description": "Professional pocket-sized dater stamp in various colors",
  "price": "120.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 11: Shiny S-724 Blue

```json
{
  "name": "Shiny S-724 Blue",
  "slug": "shiny-s-724-blue",
  "category": 1,
  "description": "Blue professional pocket-sized dater stamp",
  "short_description": "Blue professional pocket-sized dater stamp",
  "price": "120.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 12: Shiny S-724 Others

```json
{
  "name": "Shiny S-724 Others",
  "slug": "shiny-s-724-others",
  "category": 1,
  "description": "Professional pocket-sized dater stamp in various colors",
  "short_description": "Professional pocket-sized dater stamp in various colors",
  "price": "120.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

---

### Products for "Handy and Pocket Stamps" Category (Category ID: Replace with actual ID)

#### Product 13: Shiny Elite 42 Green

```json
{
  "name": "Shiny Elite 42 Green",
  "slug": "shiny-elite-42-green",
  "category": 2,
  "description": "Compact green pocket stamp for on-the-go use",
  "short_description": "Compact green pocket stamp for on-the-go use",
  "price": "100.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 14: Shiny Elite 42 Pink

```json
{
  "name": "Shiny Elite 42 Pink",
  "slug": "shiny-elite-42-pink",
  "category": 2,
  "description": "Compact pink pocket stamp for on-the-go use",
  "short_description": "Compact pink pocket stamp for on-the-go use",
  "price": "100.00",
  "stock_quantity": 100,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

---

### Products for "Heavy Duty Stamps" Category (Category ID: Replace with actual ID)

#### Product 15: Trodat Heavy 52040

```json
{
  "name": "Trodat Heavy 52040",
  "slug": "trodat-heavy-52040",
  "category": 3,
  "description": "Heavy-duty professional stamp for high-volume use",
  "short_description": "Heavy-duty professional stamp for high-volume use",
  "price": "250.00",
  "stock_quantity": 50,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 16: Trodat Heavy 54110

```json
{
  "name": "Trodat Heavy 54110",
  "slug": "trodat-heavy-54110",
  "category": 3,
  "description": "Heavy-duty professional stamp for high-volume use",
  "short_description": "Heavy-duty professional stamp for high-volume use",
  "price": "250.00",
  "stock_quantity": 50,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 17: Trodat Heavy 54120

```json
{
  "name": "Trodat Heavy 54120",
  "slug": "trodat-heavy-54120",
  "category": 3,
  "description": "Heavy-duty professional stamp for high-volume use",
  "short_description": "Heavy-duty professional stamp for high-volume use",
  "price": "250.00",
  "stock_quantity": 50,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

---

### Products for "Oval Self Ink Stamps" Category (Category ID: Replace with actual ID)

#### Product 18: Colop Printer Oval 55 Black

```json
{
  "name": "Colop Printer Oval 55 Black",
  "slug": "colop-printer-oval-55-black",
  "category": 4,
  "description": "Professional oval self-inking stamp in black",
  "short_description": "Professional oval self-inking stamp in black",
  "price": "180.00",
  "stock_quantity": 75,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 19: Colop Printer Oval 55 Blue

```json
{
  "name": "Colop Printer Oval 55 Blue",
  "slug": "colop-printer-oval-55-blue",
  "category": 4,
  "description": "Professional oval self-inking stamp in blue",
  "short_description": "Professional oval self-inking stamp in blue",
  "price": "180.00",
  "stock_quantity": 75,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 20: Colop Printer Oval 55 Red

```json
{
  "name": "Colop Printer Oval 55 Red",
  "slug": "colop-printer-oval-55-red",
  "category": 4,
  "description": "Professional oval self-inking stamp in red",
  "short_description": "Professional oval self-inking stamp in red",
  "price": "180.00",
  "stock_quantity": 75,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 21: Trodat 44055 Red

```json
{
  "name": "Trodat 44055 Red",
  "slug": "trodat-44055-red",
  "category": 4,
  "description": "Professional oval self-inking stamp in red",
  "short_description": "Professional oval self-inking stamp in red",
  "price": "180.00",
  "stock_quantity": 75,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

---

### Products for "Round Self Ink Stamps" Category (Category ID: Replace with actual ID)

#### Product 22: Trodat 46050

```json
{
  "name": "Trodat 46050",
  "slug": "trodat-46050",
  "category": 5,
  "description": "Professional round self-inking stamp",
  "short_description": "Professional round self-inking stamp",
  "price": "170.00",
  "stock_quantity": 75,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 23: Trodat 4642 Black

```json
{
  "name": "Trodat 4642 Black",
  "slug": "trodat-4642-black",
  "category": 5,
  "description": "Professional round self-inking stamp in black",
  "short_description": "Professional round self-inking stamp in black",
  "price": "170.00",
  "stock_quantity": 75,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 24: Trodat 4642 Blue

```json
{
  "name": "Trodat 4642 Blue",
  "slug": "trodat-4642-blue",
  "category": 5,
  "description": "Professional round self-inking stamp in blue",
  "short_description": "Professional round self-inking stamp in blue",
  "price": "170.00",
  "stock_quantity": 75,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

#### Product 25: Trodat 4642 Red

```json
{
  "name": "Trodat 4642 Red",
  "slug": "trodat-4642-red",
  "category": 5,
  "description": "Professional round self-inking stamp in red",
  "short_description": "Professional round self-inking stamp in red",
  "price": "170.00",
  "stock_quantity": 75,
  "track_inventory": true,
  "in_stock": true,
  "is_active": true,
  "is_featured": false
}
```

---

## Postman Setup Instructions

### 1. Authentication Setup

1. First, get your admin token by logging in:
   - **Endpoint:** `POST /api/v1/auth/login/`
   - **Payload:**
   ```json
   {
     "username": "your_admin_username",
     "password": "your_admin_password"
   }
   ```
   - Copy the `access` token from the response

2. In Postman, create a new collection or request
3. Go to the **Authorization** tab
4. Select **Bearer Token** from the Type dropdown
5. Paste your access token in the Token field
6. Or add it as a header:
   - Key: `Authorization`
   - Value: `Bearer <your_access_token>`

### 2. Headers Setup

Add these headers to all requests:
- **Content-Type:** `application/json`
- **Authorization:** `Bearer <your_access_token>`

### 3. Creating Categories

1. Set method to **POST**
2. URL: `http://localhost:8000/api/v1/categories/`
3. Copy one of the category payloads above
4. Paste in the **Body** tab (select **raw** and **JSON**)
5. Send request
6. **Important:** Copy the `id` from the response - you'll need it for products!

### 4. Creating Products

1. Set method to **POST**
2. URL: `http://localhost:8000/api/v1/products/`
3. Copy one of the product payloads above
4. Replace the `"category": 1` with the actual category ID you got from step 3
5. Paste in the **Body** tab (select **raw** and **JSON**)
6. Send request

---

## Quick Reference: Field Descriptions

### Category Fields:
- `name` (required): Category name
- `slug` (optional): URL-friendly identifier (auto-generated if not provided)
- `description` (optional): Category description
- `image` (optional): Category image (for file uploads, use form-data)
- `is_active` (optional, default: true): Whether category is active
- `order` (optional, default: 0): Display order

### Product Fields:
- `name` (required): Product name
- `slug` (required): Unique URL-friendly identifier
- `category` (required if no service): Category ID
- `service` (required if no category): Service ID
- `description` (required): Full product description
- `short_description` (optional): Brief description
- `price` (required): Base price in AED (string format: "150.00")
- `sale_price` (optional): Sale price in AED
- `stock_quantity` (optional, default: 0): Stock quantity
- `track_inventory` (optional, default: true): Whether to track inventory
- `in_stock` (optional, default: true): Stock availability status
- `sku` (optional): Stock keeping unit
- `weight` (optional): Product weight in kg
- `main_image` (optional): Main product image (for file uploads, use form-data)
- `is_active` (optional, default: true): Whether product is active
- `is_featured` (optional, default: false): Whether product is featured
- `meta_title` (optional): SEO meta title
- `meta_description` (optional): SEO meta description

---

## Notes

1. **Category IDs:** After creating categories, you'll need to update the `category` field in product payloads with the actual category IDs from the response.

2. **Prices:** All prices are in AED (UAE Dirhams). Format as strings with 2 decimal places: `"150.00"`

3. **Images:** To upload images, you'll need to use `form-data` instead of JSON and include the image file. The examples above use JSON format only.

4. **Required Fields:** Make sure all required fields are included. Missing required fields will result in validation errors.

5. **Slug Uniqueness:** Product slugs must be unique. If you get a slug conflict error, modify the slug.

