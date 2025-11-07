"""
Tests for API endpoints
"""
import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

from api.factories import (
    UserFactory, CategoryFactory, ProductFactory,
    CartFactory, OrderFactory
)

User = get_user_model()


@pytest.mark.api
class TestAuthenticationAPI:
    """Test authentication endpoints"""
    
    def test_register_user(self, api_client, db):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert 'tokens' in response.data
        assert response.data['user']['username'] == 'newuser'
    
    def test_register_user_password_mismatch(self, api_client, db):
        """Test registration with mismatched passwords"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'DifferentPass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_login_user(self, api_client, user_with_password):
        """Test user login"""
        data = {
            'username': user_with_password.username,
            'password': 'testpass123'
        }
        response = api_client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_invalid_credentials(self, api_client, user_with_password):
        """Test login with invalid credentials"""
        data = {
            'username': user_with_password.username,
            'password': 'wrongpassword'
        }
        response = api_client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_profile(self, authenticated_client, user):
        """Test getting user profile"""
        response = authenticated_client.get('/api/auth/profile/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username
        assert response.data['email'] == user.email
    
    def test_get_profile_unauthenticated(self, api_client):
        """Test getting profile without authentication"""
        response = api_client.get('/api/auth/profile/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.api
class TestCategoryAPI:
    """Test category endpoints"""
    
    def test_list_categories(self, api_client, categories):
        """Test listing categories"""
        response = api_client.get('/api/categories/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 5
    
    def test_retrieve_category(self, api_client, category):
        """Test retrieving a single category"""
        response = api_client.get(f'/api/categories/{category.slug}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == category.name
    
    def test_create_category_as_admin(self, admin_client, db):
        """Test creating a category as admin"""
        data = {
            'name': 'New Category',
            'slug': 'new-category',
            'description': 'Test description',
            'is_active': True,
            'order': 1
        }
        response = admin_client.post('/api/categories/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Category'
    
    def test_create_category_as_regular_user(self, authenticated_client, db):
        """Test that regular users cannot create categories"""
        data = {
            'name': 'New Category',
            'slug': 'new-category'
        }
        response = authenticated_client.post('/api/categories/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api
class TestProductAPI:
    """Test product endpoints"""
    
    def test_list_products(self, api_client, products):
        """Test listing products"""
        response = api_client.get('/api/products/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) >= 1
    
    def test_retrieve_product(self, api_client, product):
        """Test retrieving a single product"""
        response = api_client.get(f'/api/products/{product.slug}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == product.name
        assert 'category' in response.data
    
    def test_list_featured_products(self, api_client, featured_products):
        """Test listing featured products"""
        response = api_client.get('/api/products/featured/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        for product in response.data:
            assert product['is_featured'] is True
    
    def test_search_products(self, api_client, db):
        """Test product search"""
        product = ProductFactory(name='Special Test Product')
        response = api_client.get('/api/products/search/', {'q': 'Special'})
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
    
    def test_filter_products_by_category(self, api_client, category, products):
        """Test filtering products by category"""
        response = api_client.get('/api/products/', {'category': category.id})
        assert response.status_code == status.HTTP_200_OK
        for product in response.data['results']:
            assert product['category'] == category.id


@pytest.mark.api
class TestCartAPI:
    """Test cart endpoints"""
    
    def test_get_cart(self, authenticated_client, user):
        """Test getting user's cart"""
        response = authenticated_client.get('/api/cart/')
        assert response.status_code == status.HTTP_200_OK
        assert 'items' in response.data
        assert 'subtotal' in response.data
    
    def test_get_cart_unauthenticated(self, api_client):
        """Test that unauthenticated users cannot access cart"""
        response = api_client.get('/api/cart/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_add_item_to_cart(self, authenticated_client, product):
        """Test adding item to cart"""
        data = {
            'product_id': product.id,
            'quantity': 2
        }
        response = authenticated_client.post('/api/cart/add_item/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'cart' in response.data
        assert response.data['cart']['total_items'] == 2
    
    def test_add_invalid_product_to_cart(self, authenticated_client):
        """Test adding non-existent product to cart"""
        data = {
            'product_id': 99999,
            'quantity': 1
        }
        response = authenticated_client.post('/api/cart/add_item/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_clear_cart(self, authenticated_client, cart_with_items):
        """Test clearing cart"""
        response = authenticated_client.post('/api/cart/clear/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['cart']['total_items'] == 0


@pytest.mark.api
class TestOrderAPI:
    """Test order endpoints"""
    
    def test_list_orders(self, authenticated_client, user, db):
        """Test listing user's orders"""
        OrderFactory.create_batch(3, user=user)
        response = authenticated_client.get('/api/orders/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 3
    
    def test_list_orders_only_own(self, authenticated_client, user, db):
        """Test that users only see their own orders"""
        OrderFactory.create_batch(2, user=user)
        other_user = UserFactory()
        OrderFactory.create_batch(3, user=other_user)
        
        response = authenticated_client.get('/api/orders/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2  # Only user's orders
    
    def test_retrieve_order(self, authenticated_client, order_with_items):
        """Test retrieving a single order"""
        response = authenticated_client.get(f'/api/orders/{order_with_items.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['order_number'] == order_with_items.order_number
        assert 'items' in response.data
    
    def test_checkout_from_cart(self, authenticated_client, cart_with_items):
        """Test creating order from cart"""
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
        assert response.status_code == status.HTTP_201_CREATED
        assert 'order_number' in response.data
        assert response.data['status'] == 'pending'


@pytest.mark.api
class TestAdminAPI:
    """Test admin endpoints"""
    
    def test_admin_statistics(self, admin_client, db):
        """Test admin statistics endpoint"""
        # Create some data
        UserFactory.create_batch(5)
        ProductFactory.create_batch(10)
        OrderFactory.create_batch(3)
        
        response = admin_client.get('/api/admin/statistics/')
        assert response.status_code == status.HTTP_200_OK
        assert 'orders' in response.data
        assert 'revenue' in response.data
        assert 'products' in response.data
        assert 'users' in response.data
    
    def test_admin_statistics_unauthorized(self, authenticated_client):
        """Test that regular users cannot access admin statistics"""
        response = authenticated_client.get('/api/admin/statistics/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

