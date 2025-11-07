"""
Pytest configuration and fixtures
"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from api.factories import (
    UserFactory, AdminUserFactory,
    CategoryFactory, ProductFactory, FeaturedProductFactory,
    CartFactory, OrderFactory,
    create_complete_product, create_complete_order, create_cart_with_items
)

User = get_user_model()


# ============ User Fixtures ============

@pytest.fixture
def user(db):
    """Create a regular user"""
    return UserFactory()


@pytest.fixture
def admin_user(db):
    """Create an admin user"""
    return AdminUserFactory()


@pytest.fixture
def user_with_password(db):
    """Create a user with known password"""
    return UserFactory(password='testpass123')


# ============ API Client Fixtures ============

@pytest.fixture
def api_client():
    """Create an anonymous API client"""
    return APIClient()


@pytest.fixture
def authenticated_client(user):
    """Create an authenticated API client"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def admin_client(admin_user):
    """Create an admin authenticated API client"""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


# ============ Model Fixtures ============

@pytest.fixture
def category(db):
    """Create a category"""
    return CategoryFactory()


@pytest.fixture
def categories(db):
    """Create multiple categories"""
    return CategoryFactory.create_batch(5)


@pytest.fixture
def product(db, category):
    """Create a product"""
    return ProductFactory(category=category)


@pytest.fixture
def products(db, category):
    """Create multiple products"""
    return ProductFactory.create_batch(10, category=category)


@pytest.fixture
def featured_products(db, category):
    """Create featured products"""
    return FeaturedProductFactory.create_batch(5, category=category)


@pytest.fixture
def complete_product(db):
    """Create a complete product with images and specs"""
    return create_complete_product(with_images=True, with_specs=True, with_variants=True)


@pytest.fixture
def cart(db, user):
    """Create a cart for user"""
    return CartFactory(user=user)


@pytest.fixture
def cart_with_items(db, user):
    """Create a cart with items"""
    return create_cart_with_items(user=user, items_count=3)


@pytest.fixture
def order(db, user):
    """Create an order"""
    return OrderFactory(user=user)


@pytest.fixture
def order_with_items(db, user):
    """Create an order with items"""
    return create_complete_order(with_items=True, with_files=False, items_count=3)


@pytest.fixture
def completed_order(db, user):
    """Create a completed order"""
    from api.factories import CompletedOrderFactory
    return CompletedOrderFactory(user=user)


# ============ JWT Token Fixtures ============

@pytest.fixture
def user_tokens(user_with_password, api_client):
    """Get JWT tokens for a user"""
    response = api_client.post('/api/auth/login/', {
        'username': user_with_password.username,
        'password': 'testpass123'
    })
    return response.data


@pytest.fixture
def auth_headers(user_tokens):
    """Get authentication headers with JWT token"""
    return {
        'HTTP_AUTHORIZATION': f'Bearer {user_tokens["access"]}'
    }

