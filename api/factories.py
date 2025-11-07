"""
Factory Boy factories for creating test data
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import (
    Category, Product, ProductImage, ProductSpecification, ProductVariant,
    Cart, CartItem, Order, OrderItem, OrderFile
)

User = get_user_model()
fake = Faker()


# ============ User Factory ============

class UserFactory(DjangoModelFactory):
    """Factory for creating users"""
    
    class Meta:
        model = User
        django_get_or_create = ('username',)
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone = factory.Faker('phone_number')
    address = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.Faker('state')
    country = 'UAE'
    company_name = factory.Faker('company')
    is_active = True
    is_staff = False
    is_superuser = False
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Set password after user creation"""
        if not create:
            return
        
        password = extracted or 'testpass123'
        self.set_password(password)
        self.save()


class AdminUserFactory(UserFactory):
    """Factory for creating admin users"""
    
    username = factory.Sequence(lambda n: f'admin{n}')
    is_staff = True
    is_superuser = True


# ============ Category Factory ============

class CategoryFactory(DjangoModelFactory):
    """Factory for creating categories"""
    
    class Meta:
        model = Category
        django_get_or_create = ('slug',)
    
    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(' ', '-'))
    description = factory.Faker('text', max_nb_chars=200)
    is_active = True
    order = factory.Sequence(lambda n: n)
    parent = None


class SubCategoryFactory(CategoryFactory):
    """Factory for creating subcategories"""
    
    parent = factory.SubFactory(CategoryFactory)


# ============ Product Factories ============

class ProductFactory(DjangoModelFactory):
    """Factory for creating products"""
    
    class Meta:
        model = Product
        django_get_or_create = ('slug',)
    
    name = factory.Faker('catch_phrase')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(' ', '-')[:50])
    category = factory.SubFactory(CategoryFactory)
    description = factory.Faker('text', max_nb_chars=500)
    short_description = factory.Faker('text', max_nb_chars=150)
    price = factory.LazyFunction(lambda: Decimal(fake.random_int(min=50, max=500)))
    sale_price = None
    stock_quantity = factory.Faker('random_int', min=0, max=100)
    track_inventory = True
    in_stock = True
    sku = factory.Sequence(lambda n: f'SKU-{n:05d}')
    weight = factory.LazyFunction(lambda: Decimal(fake.random_int(min=1, max=50)) / 10)
    is_active = True
    is_featured = factory.Faker('boolean', chance_of_getting_true=30)
    meta_title = factory.LazyAttribute(lambda obj: obj.name)
    meta_description = factory.LazyAttribute(lambda obj: obj.short_description)


class FeaturedProductFactory(ProductFactory):
    """Factory for creating featured products"""
    
    is_featured = True


class ProductOnSaleFactory(ProductFactory):
    """Factory for creating products on sale"""
    
    sale_price = factory.LazyAttribute(
        lambda obj: Decimal(float(obj.price) * 0.8)  # 20% discount
    )


class ProductImageFactory(DjangoModelFactory):
    """Factory for creating product images"""
    
    class Meta:
        model = ProductImage
    
    product = factory.SubFactory(ProductFactory)
    # Note: For actual file upload testing, you'd need to use factory.django.ImageField
    # image = factory.django.ImageField(color='blue')
    alt_text = factory.Faker('sentence', nb_words=4)
    order = factory.Sequence(lambda n: n)


class ProductSpecificationFactory(DjangoModelFactory):
    """Factory for creating product specifications"""
    
    class Meta:
        model = ProductSpecification
    
    product = factory.SubFactory(ProductFactory)
    key = factory.Faker('word')
    value = factory.Faker('sentence', nb_words=3)
    order = factory.Sequence(lambda n: n)


class ProductVariantFactory(DjangoModelFactory):
    """Factory for creating product variants"""
    
    class Meta:
        model = ProductVariant
    
    product = factory.SubFactory(ProductFactory)
    name = factory.Faker('color_name')
    sku = factory.Sequence(lambda n: f'VAR-{n:05d}')
    price_adjustment = factory.LazyFunction(lambda: Decimal(fake.random_int(min=0, max=50)))
    stock_quantity = factory.Faker('random_int', min=0, max=50)
    is_active = True


# ============ Cart Factories ============

class CartFactory(DjangoModelFactory):
    """Factory for creating carts"""
    
    class Meta:
        model = Cart
    
    user = factory.SubFactory(UserFactory)
    session_id = None


class GuestCartFactory(CartFactory):
    """Factory for creating guest carts"""
    
    user = None
    session_id = factory.Faker('uuid4')


class CartItemFactory(DjangoModelFactory):
    """Factory for creating cart items"""
    
    class Meta:
        model = CartItem
    
    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    variant = None
    quantity = factory.Faker('random_int', min=1, max=5)
    price = factory.LazyAttribute(lambda obj: obj.product.current_price)


# ============ Order Factories ============

class OrderFactory(DjangoModelFactory):
    """Factory for creating orders"""
    
    class Meta:
        model = Order
    
    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    company_name = factory.Faker('company')
    address_line_1 = factory.Faker('street_address')
    address_line_2 = factory.Faker('secondary_address')
    city = factory.Faker('city')
    state = factory.Faker('state')
    country = 'UAE'
    postal_code = factory.Faker('postcode')
    order_notes = factory.Faker('text', max_nb_chars=200)
    subtotal = factory.LazyFunction(lambda: Decimal(fake.random_int(min=100, max=1000)))
    shipping_cost = Decimal('0.00')
    tax = Decimal('0.00')
    total = factory.LazyAttribute(lambda obj: obj.subtotal + obj.shipping_cost + obj.tax)
    status = 'pending'
    payment_status = 'pending'


class ConfirmedOrderFactory(OrderFactory):
    """Factory for creating confirmed orders"""
    
    status = 'confirmed'
    confirmed_at = factory.Faker('date_time_this_month')


class CompletedOrderFactory(OrderFactory):
    """Factory for creating completed orders"""
    
    status = 'delivered'
    payment_status = 'paid'
    confirmed_at = factory.Faker('date_time_this_month')
    shipped_at = factory.Faker('date_time_this_month')
    delivered_at = factory.Faker('date_time_this_month')


class OrderItemFactory(DjangoModelFactory):
    """Factory for creating order items"""
    
    class Meta:
        model = OrderItem
    
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    product_name = factory.LazyAttribute(lambda obj: obj.product.name)
    variant = None
    variant_name = None
    quantity = factory.Faker('random_int', min=1, max=5)
    price = factory.LazyAttribute(lambda obj: obj.product.current_price)
    total = factory.LazyAttribute(lambda obj: obj.price * obj.quantity)


class OrderFileFactory(DjangoModelFactory):
    """Factory for creating order files"""
    
    class Meta:
        model = OrderFile
    
    order = factory.SubFactory(OrderFactory)
    # Note: For actual file upload testing, you'd need to use factory.django.FileField
    file_name = factory.Faker('file_name', extension='pdf')
    file_type = factory.Faker('random_element', elements=['emiratesId', 'tradeLicense', 'specificDesign'])
    file_size = factory.Faker('random_int', min=1000, max=10000000)  # 1KB to 10MB
    product_name = factory.Faker('catch_phrase')
    description = factory.Faker('sentence')


# ============ Helper Functions ============

def create_complete_product(with_images=True, with_specs=True, with_variants=False):
    """Create a complete product with related objects"""
    product = ProductFactory()
    
    if with_images:
        ProductImageFactory.create_batch(3, product=product)
    
    if with_specs:
        ProductSpecificationFactory.create_batch(5, product=product, 
            key=factory.Iterator(['Size', 'Material', 'Color', 'Weight', 'Dimensions']))
    
    if with_variants:
        ProductVariantFactory.create_batch(3, product=product)
    
    return product


def create_complete_order(with_items=True, with_files=False, items_count=3):
    """Create a complete order with items and files"""
    order = OrderFactory()
    
    if with_items:
        order_items = OrderItemFactory.create_batch(items_count, order=order)
        # Update order total based on items
        order.subtotal = sum(item.total for item in order_items)
        order.total = order.subtotal + order.shipping_cost + order.tax
        order.save()
    
    if with_files:
        OrderFileFactory.create_batch(2, order=order)
    
    return order


def create_cart_with_items(user=None, items_count=3):
    """Create a cart with items"""
    if user:
        cart = CartFactory(user=user)
    else:
        cart = GuestCartFactory()
    
    CartItemFactory.create_batch(items_count, cart=cart)
    
    return cart

