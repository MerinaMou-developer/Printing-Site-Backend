"""
Tests for models
"""
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model

from api.factories import (
    UserFactory, CategoryFactory, ProductFactory,
    CartFactory, CartItemFactory, OrderFactory, OrderItemFactory
)

User = get_user_model()


@pytest.mark.unit
class TestUserModel:
    """Test User model"""
    
    def test_create_user(self, db):
        """Test creating a user"""
        user = UserFactory()
        assert user.id is not None
        assert user.username is not None
        assert user.email is not None
    
    def test_user_string_representation(self, db):
        """Test user __str__ method"""
        user = UserFactory(username='testuser')
        assert str(user) == 'testuser'
    
    def test_user_password_is_hashed(self, db):
        """Test that password is properly hashed"""
        user = UserFactory(password='testpass123')
        assert user.password != 'testpass123'
        assert user.check_password('testpass123')


@pytest.mark.unit
class TestCategoryModel:
    """Test Category model"""
    
    def test_create_category(self, db):
        """Test creating a category"""
        category = CategoryFactory()
        assert category.id is not None
        assert category.name is not None
        assert category.slug is not None
    
    def test_category_string_representation(self, db):
        """Test category __str__ method"""
        category = CategoryFactory(name='Test Category')
        assert str(category) == 'Test Category'
    
    def test_category_with_parent(self, db):
        """Test creating a subcategory"""
        parent = CategoryFactory(name='Parent')
        child = CategoryFactory(name='Child', parent=parent)
        assert child.parent == parent
        assert child in parent.children.all()


@pytest.mark.unit
class TestProductModel:
    """Test Product model"""
    
    def test_create_product(self, db):
        """Test creating a product"""
        product = ProductFactory()
        assert product.id is not None
        assert product.name is not None
        assert product.slug is not None
        assert product.category is not None
    
    def test_product_string_representation(self, db):
        """Test product __str__ method"""
        product = ProductFactory(name='Test Product')
        assert str(product) == 'Test Product'
    
    def test_product_current_price_regular(self, db):
        """Test current_price property with regular price"""
        product = ProductFactory(price=Decimal('100.00'), sale_price=None)
        assert product.current_price == Decimal('100.00')
    
    def test_product_current_price_on_sale(self, db):
        """Test current_price property with sale price"""
        product = ProductFactory(
            price=Decimal('100.00'),
            sale_price=Decimal('80.00')
        )
        assert product.current_price == Decimal('80.00')


@pytest.mark.unit
class TestCartModel:
    """Test Cart model"""
    
    def test_create_cart(self, db):
        """Test creating a cart"""
        cart = CartFactory()
        assert cart.id is not None
        assert cart.user is not None
    
    def test_cart_total_items(self, db):
        """Test cart total_items property"""
        cart = CartFactory()
        CartItemFactory.create_batch(3, cart=cart, quantity=2)
        assert cart.total_items == 6  # 3 items × 2 quantity
    
    def test_cart_subtotal(self, db):
        """Test cart subtotal property"""
        cart = CartFactory()
        product1 = ProductFactory(price=Decimal('100.00'))
        product2 = ProductFactory(price=Decimal('50.00'))
        CartItemFactory(cart=cart, product=product1, quantity=2, price=product1.price)
        CartItemFactory(cart=cart, product=product2, quantity=1, price=product2.price)
        assert cart.subtotal == Decimal('250.00')  # (100×2) + (50×1)


@pytest.mark.unit
class TestCartItemModel:
    """Test CartItem model"""
    
    def test_create_cart_item(self, db):
        """Test creating a cart item"""
        item = CartItemFactory()
        assert item.id is not None
        assert item.cart is not None
        assert item.product is not None
    
    def test_cart_item_total_price(self, db):
        """Test cart item total_price property"""
        item = CartItemFactory(price=Decimal('100.00'), quantity=3)
        assert item.total_price == Decimal('300.00')
    
    def test_cart_item_price_auto_set(self, db):
        """Test that price is automatically set from product"""
        product = ProductFactory(price=Decimal('150.00'))
        item = CartItemFactory(product=product, price=None)
        # Price should be set in save method
        assert item.price == product.current_price


@pytest.mark.unit
class TestOrderModel:
    """Test Order model"""
    
    def test_create_order(self, db):
        """Test creating an order"""
        order = OrderFactory()
        assert order.id is not None
        assert order.order_number is not None
        assert order.first_name is not None
    
    def test_order_number_auto_generated(self, db):
        """Test that order number is automatically generated"""
        order = OrderFactory()
        assert order.order_number.startswith('ORD-')
    
    def test_order_full_name(self, db):
        """Test order full_name property"""
        order = OrderFactory(first_name='John', last_name='Doe')
        assert order.full_name == 'John Doe'
    
    def test_order_full_address(self, db):
        """Test order full_address property"""
        order = OrderFactory(
            address_line_1='123 Main St',
            city='Dubai',
            country='UAE'
        )
        assert 'Dubai' in order.full_address
        assert 'UAE' in order.full_address


@pytest.mark.unit
class TestOrderItemModel:
    """Test OrderItem model"""
    
    def test_create_order_item(self, db):
        """Test creating an order item"""
        item = OrderItemFactory()
        assert item.id is not None
        assert item.order is not None
        assert item.product is not None
    
    def test_order_item_total_calculation(self, db):
        """Test that total is calculated on save"""
        item = OrderItemFactory(price=Decimal('75.00'), quantity=4)
        assert item.total == Decimal('300.00')

