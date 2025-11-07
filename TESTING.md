# PrintPro API - Testing Guide

Complete guide for testing your Django REST API using pytest and Factory Boy.

## 🧪 Testing Stack

- **pytest** - Modern, powerful testing framework
- **pytest-django** - Django integration for pytest
- **Factory Boy** - Generate test data easily
- **Faker** - Realistic fake data generation

## 📦 What's Included

### ✅ 30+ Tests Created
- **Model Tests** (22 tests) - Test all database models
- **API Tests** (30+ tests) - Test all API endpoints
- **Factories** - Generate realistic test data
- **Fixtures** - Reusable test components
- **Sample Data Command** - Create data instantly

## 🚀 Quick Start

### Run All Tests
```bash
cd printing-api
pytest
```

### Run Specific Test File
```bash
pytest api/tests/test_models.py
pytest api/tests/test_api.py
```

### Run With Verbose Output
```bash
pytest -v
```

### Run Specific Test Class
```bash
pytest api/tests/test_models.py::TestUserModel
```

### Run Specific Test
```bash
pytest api/tests/test_models.py::TestUserModel::test_create_user
```

### Run Tests by Marker
```bash
# Run only unit tests
pytest -m unit

# Run only API tests
pytest -m api

# Run only integration tests
pytest -m integration
```

## 📊 Test Coverage

### Model Tests (`test_models.py`)
- ✅ User model (3 tests)
- ✅ Category model (3 tests)
- ✅ Product model (4 tests)
- ✅ Cart model (3 tests)
- ✅ CartItem model (3 tests)
- ✅ Order model (4 tests)
- ✅ OrderItem model (2 tests)

### API Tests (`test_api.py`)
- ✅ Authentication endpoints (6 tests)
- ✅ Category endpoints (4 tests)
- ✅ Product endpoints (5 tests)
- ✅ Cart endpoints (5 tests)
- ✅ Order endpoints (4 tests)
- ✅ Admin endpoints (2 tests)

## 🏭 Factory Boy - Generate Test Data

### Using Factories

#### Create a User
```python
from api.factories import UserFactory

# Create a user
user = UserFactory()

# Create with specific data
user = UserFactory(username='johndoe', email='john@example.com')

# Create with password
user = UserFactory(password='testpass123')

# Create multiple users
users = UserFactory.create_batch(10)
```

#### Create Products
```python
from api.factories import ProductFactory, FeaturedProductFactory

# Create a product
product = ProductFactory()

# Create featured product
product = FeaturedProductFactory()

# Create with specific category
from api.factories import CategoryFactory
category = CategoryFactory(name='Stamps')
product = ProductFactory(category=category)

# Create complete product with images, specs, variants
from api.factories import create_complete_product
product = create_complete_product(
    with_images=True,
    with_specs=True,
    with_variants=True
)
```

#### Create Orders
```python
from api.factories import OrderFactory, create_complete_order

# Simple order
order = OrderFactory()

# Complete order with items
order = create_complete_order(
    with_items=True,
    with_files=True,
    items_count=5
)
```

#### Create Cart with Items
```python
from api.factories import create_cart_with_items

user = UserFactory()
cart = create_cart_with_items(user=user, items_count=3)
```

## 🔧 pytest Fixtures

### Available Fixtures (from `conftest.py`)

#### User Fixtures
```python
def test_something(user):
    # user is a regular user
    assert user.is_staff == False

def test_admin(admin_user):
    # admin_user is an admin
    assert admin_user.is_superuser == True

def test_with_password(user_with_password):
    # user with known password 'testpass123'
    assert user_with_password.check_password('testpass123')
```

#### API Client Fixtures
```python
def test_public(api_client):
    # Anonymous API client
    response = api_client.get('/api/products/')
    assert response.status_code == 200

def test_authenticated(authenticated_client):
    # Authenticated API client
    response = authenticated_client.get('/api/cart/')
    assert response.status_code == 200

def test_admin_endpoint(admin_client):
    # Admin authenticated client
    response = admin_client.get('/api/admin/statistics/')
    assert response.status_code == 200
```

#### Model Fixtures
```python
def test_with_products(products):
    # products is a list of 10 products
    assert len(products) == 10

def test_with_cart(cart_with_items):
    # cart with 3 items
    assert cart_with_items.total_items == 3

def test_with_order(order_with_items):
    # order with items
    assert order_with_items.items.count() > 0
```

## 📝 Writing Tests

### Example: Test Model
```python
import pytest
from api.factories import ProductFactory

@pytest.mark.unit
class TestProductModel:
    def test_create_product(self, db):
        """Test creating a product"""
        product = ProductFactory()
        assert product.id is not None
        assert product.name is not None
    
    def test_product_price(self, db):
        """Test product pricing"""
        product = ProductFactory(
            price=100,
            sale_price=80
        )
        assert product.current_price == 80
```

### Example: Test API Endpoint
```python
import pytest
from rest_framework import status

@pytest.mark.api
class TestProductAPI:
    def test_list_products(self, api_client, products):
        """Test listing products"""
        response = api_client.get('/api/products/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
    
    def test_create_product_as_admin(self, admin_client, category):
        """Test creating product as admin"""
        data = {
            'name': 'New Product',
            'slug': 'new-product',
            'category_id': category.id,
            'price': '100.00',
            'description': 'Test product'
        }
        response = admin_client.post('/api/products/', data)
        assert response.status_code == status.HTTP_201_CREATED
```

## 🎯 Generate Sample Data

### Using Management Command

#### Create Default Data
```bash
python manage.py create_sample_data
```

This creates:
- 10 users (including admin and testuser)
- 8 categories
- 30 products
- 5 carts with items
- 15 orders

#### Custom Amounts
```bash
# Create custom amounts
python manage.py create_sample_data --users 20 --products 50 --orders 30

# Clear existing data first
python manage.py create_sample_data --clear
```

#### Test Credentials
After running the command, you'll have:
- **Admin**: `admin` / `admin123`
- **Test User**: `testuser` / `testpass123`

### Quick Data Summary
```bash
python manage.py create_sample_data
```

Output includes:
```
Data Summary:
  Users: 21 total
    - Admins: 1
    - Regular: 20
  Categories: 8
  Products: 40
  Carts: 5
  Orders: 20
```

## 🔍 Test Examples

### Test User Registration
```python
def test_register_user(api_client, db):
    data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'SecurePass123',
        'password_confirm': 'SecurePass123',
        'first_name': 'New',
        'last_name': 'User'
    }
    response = api_client.post('/api/auth/register/', data)
    assert response.status_code == 201
    assert 'tokens' in response.data
```

### Test Product Listing
```python
def test_list_products(api_client, products):
    response = api_client.get('/api/products/')
    assert response.status_code == 200
    assert len(response.data['results']) >= 1
```

### Test Cart Operations
```python
def test_add_to_cart(authenticated_client, product):
    data = {'product_id': product.id, 'quantity': 2}
    response = authenticated_client.post('/api/cart/add_item/', data)
    assert response.status_code == 201
    assert response.data['cart']['total_items'] == 2
```

### Test Order Creation
```python
def test_checkout(authenticated_client, cart_with_items):
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '+971501234567',
        'address_line_1': '123 Main St',
        'city': 'Dubai',
        'country': 'UAE'
    }
    response = authenticated_client.post('/api/orders/checkout/', data)
    assert response.status_code == 201
    assert 'order_number' in response.data
```

## 📋 pytest Configuration (`pytest.ini`)

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
addopts = --verbose --strict-markers --tb=short --no-migrations --reuse-db
markers =
    unit: Unit tests
    integration: Integration tests
    api: API endpoint tests
    slow: Slow running tests
```

## 🎨 Best Practices

### 1. Use Factories
```python
# Good - Using factory
user = UserFactory()

# Bad - Manual creation
user = User.objects.create(
    username='test',
    email='test@example.com',
    # ... many more fields
)
```

### 2. Use Fixtures
```python
# Good - Using fixture
def test_something(authenticated_client):
    response = authenticated_client.get('/api/cart/')

# Bad - Manual setup in every test
def test_something():
    user = User.objects.create(...)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/cart/')
```

### 3. Mark Your Tests
```python
@pytest.mark.unit
def test_model():
    pass

@pytest.mark.api
def test_endpoint():
    pass
```

### 4. Test One Thing
```python
# Good - Tests one thing
def test_user_can_login():
    # Test login logic only
    pass

# Bad - Tests multiple things
def test_user_workflow():
    # Login, create cart, add items, checkout...
    pass
```

## 🚀 Running Tests in CI/CD

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest
```

## 📊 Test Results

After running tests, you'll see:
```
===================== test session starts ======================
collected 52 items

api/tests/test_models.py ...................... [ 42%]
api/tests/test_api.py .......................... [100%]

===================== 52 passed in 15.23s ======================
```

## 🎯 Next Steps

1. **Run Tests**: `pytest -v`
2. **Generate Data**: `python manage.py create_sample_data`
3. **Write More Tests**: Add tests for your custom features
4. **Test Coverage**: `pytest --cov=api`
5. **Continuous Integration**: Set up CI/CD with tests

## 🔗 Useful Commands

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Run specific markers
pytest -m unit
pytest -m api

# Run failed tests only
pytest --lf

# Create test database
pytest --create-db

# Parallel execution (requires pytest-xdist)
pytest -n auto
```

## 📚 Learn More

- pytest: https://docs.pytest.org/
- pytest-django: https://pytest-django.readthedocs.io/
- Factory Boy: https://factoryboy.readthedocs.io/
- Faker: https://faker.readthedocs.io/

---

**Your API now has professional testing! 🧪✅**

Run `pytest -v` to see all tests passing!

