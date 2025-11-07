"""
Management command to create sample data for the printing API

Usage:
    python manage.py create_sample_data
    python manage.py create_sample_data --users 10 --products 50
    python manage.py create_sample_data --clear
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from api.models import (
    Category, Product, ProductImage, ProductSpecification, ProductVariant,
    Cart, CartItem, Order, OrderItem
)
from api.factories import (
    UserFactory, AdminUserFactory,
    CategoryFactory, SubCategoryFactory,
    ProductFactory, FeaturedProductFactory, ProductOnSaleFactory,
    ProductImageFactory, ProductSpecificationFactory, ProductVariantFactory,
    CartFactory, CartItemFactory,
    OrderFactory, ConfirmedOrderFactory, CompletedOrderFactory,
    OrderItemFactory,
    create_complete_product, create_complete_order, create_cart_with_items
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for the printing API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create'
        )
        parser.add_argument(
            '--categories',
            type=int,
            default=8,
            help='Number of categories to create'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=30,
            help='Number of products to create'
        )
        parser.add_argument(
            '--orders',
            type=int,
            default=15,
            help='Number of orders to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            self.clear_data()
            self.stdout.write(self.style.SUCCESS('[OK] Data cleared'))

        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create users
        users_count = options['users']
        self.create_users(users_count)
        
        # Create categories
        categories_count = options['categories']
        categories = self.create_categories(categories_count)
        
        # Create products
        products_count = options['products']
        self.create_products(products_count, categories)
        
        # Create carts with items
        self.create_carts()
        
        # Create orders
        orders_count = options['orders']
        self.create_orders(orders_count)
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('[SUCCESS] Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.print_summary()

    def clear_data(self):
        """Clear existing data (except superusers)"""
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        ProductVariant.objects.all().delete()
        ProductSpecification.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    def create_users(self, count):
        """Create sample users"""
        self.stdout.write(f'Creating {count} users...')
        
        # Create admin user (if doesn't exist)
        if not User.objects.filter(username='admin').exists():
            admin = AdminUserFactory(
                username='admin',
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS(f'  [+] Admin user created: admin / admin123'))
        
        # Create test user (if doesn't exist)
        if not User.objects.filter(username='testuser').exists():
            test_user = UserFactory(
                username='testuser',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password='testpass123'
            )
            self.stdout.write(self.style.SUCCESS(f'  [+] Test user created: testuser / testpass123'))
        
        # Create regular users
        users = UserFactory.create_batch(count - 2)
        self.stdout.write(self.style.SUCCESS(f'  [+] Created {len(users)} regular users'))

    def create_categories(self, count):
        """Create sample categories"""
        self.stdout.write(f'Creating {count} categories...')
        
        # Create main categories
        categories = [
            ('Dater Stamp Products', 'dater-stamp-products', 'Professional dater stamps with customizable text'),
            ('Handy and Pocket Stamps', 'handy-pocket-stamps', 'Compact portable stamps for on-the-go use'),
            ('Heavy Duty Stamps', 'heavy-duty-stamps', 'Industrial-grade stamps for high-volume use'),
            ('Oval Self Ink Stamps', 'oval-self-ink-stamps', 'Professional oval self-inking stamps'),
            ('Round Self Ink Stamps', 'round-self-ink-stamps', 'Circular self-inking stamps'),
            ('Digital Printing', 'digital-printing', 'High-quality digital printing services'),
            ('Screen Printing', 'screen-printing', 'Professional screen printing for textiles'),
            ('Office Supplies', 'office-supplies', 'Essential office supplies and stationery'),
        ]
        
        created_categories = []
        for name, slug, desc in categories[:count]:
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': desc, 'is_active': True}
            )
            created_categories.append(category)
            if created:
                self.stdout.write(f'  [+] Created category: {name}')
        
        # Create some subcategories
        if len(created_categories) > 2:
            SubCategoryFactory(parent=created_categories[0], name='Date Stamps', slug='date-stamps')
            SubCategoryFactory(parent=created_categories[0], name='Time Stamps', slug='time-stamps')
            self.stdout.write('  [+] Created subcategories')
        
        return created_categories

    def create_products(self, count, categories):
        """Create sample products"""
        self.stdout.write(f'Creating {count} products...')
        
        products_data = []
        
        # Create complete products (with images, specs, variants)
        complete_count = min(10, count // 3)
        for i in range(complete_count):
            category = categories[i % len(categories)]
            product = create_complete_product(
                with_images=False,  # Skip images for now
                with_specs=True,
                with_variants=(i % 2 == 0)  # Every other product has variants
            )
            product.category = category
            product.save()
            products_data.append(product)
        
        # Create featured products
        featured_count = min(8, count // 4)
        for category in categories[:featured_count]:
            product = FeaturedProductFactory(category=category)
            products_data.append(product)
        
        # Create products on sale
        sale_count = min(5, count // 5)
        for i in range(sale_count):
            category = categories[i % len(categories)]
            product = ProductOnSaleFactory(category=category)
            products_data.append(product)
        
        # Create regular products
        remaining = count - len(products_data)
        if remaining > 0:
            for i in range(remaining):
                category = categories[i % len(categories)]
                product = ProductFactory(category=category)
                products_data.append(product)
        
        self.stdout.write(self.style.SUCCESS(f'  [+] Created {len(products_data)} products'))
        self.stdout.write(f'    - {complete_count} complete products (with specs)')
        self.stdout.write(f'    - {featured_count} featured products')
        self.stdout.write(f'    - {sale_count} products on sale')

    def create_carts(self):
        """Create sample carts"""
        self.stdout.write('Creating sample carts...')
        
        # Get some users
        users = User.objects.filter(is_superuser=False)[:5]
        
        for user in users:
            cart = create_cart_with_items(user=user, items_count=3)
            self.stdout.write(f'  [+] Created cart for {user.username} with {cart.total_items} items')

    def create_orders(self, count):
        """Create sample orders"""
        self.stdout.write(f'Creating {count} orders...')
        
        users = list(User.objects.filter(is_superuser=False))
        if not users:
            self.stdout.write(self.style.WARNING('  No users available for orders'))
            return
        
        # Create orders with different statuses
        pending_count = count // 3
        confirmed_count = count // 3
        completed_count = count - pending_count - confirmed_count
        
        # Pending orders
        for i in range(pending_count):
            user = users[i % len(users)]
            order = create_complete_order(with_items=True, with_files=False, items_count=3)
            order.user = user
            order.save()
        
        # Confirmed orders
        for i in range(confirmed_count):
            user = users[i % len(users)]
            order = ConfirmedOrderFactory(user=user)
            OrderItemFactory.create_batch(2, order=order)
        
        # Completed orders
        for i in range(completed_count):
            user = users[i % len(users)]
            order = CompletedOrderFactory(user=user)
            OrderItemFactory.create_batch(3, order=order)
        
        self.stdout.write(self.style.SUCCESS(f'  [+] Created {count} orders'))
        self.stdout.write(f'    - {pending_count} pending orders')
        self.stdout.write(f'    - {confirmed_count} confirmed orders')
        self.stdout.write(f'    - {completed_count} completed orders')

    def print_summary(self):
        """Print summary of created data"""
        self.stdout.write('\nData Summary:')
        self.stdout.write(f'  Users: {User.objects.count()} total')
        self.stdout.write(f'    - Admins: {User.objects.filter(is_superuser=True).count()}')
        self.stdout.write(f'    - Regular: {User.objects.filter(is_superuser=False).count()}')
        self.stdout.write(f'  Categories: {Category.objects.count()}')
        self.stdout.write(f'  Products: {Product.objects.count()}')
        self.stdout.write(f'    - Active: {Product.objects.filter(is_active=True).count()}')
        self.stdout.write(f'    - Featured: {Product.objects.filter(is_featured=True).count()}')
        self.stdout.write(f'  Carts: {Cart.objects.count()}')
        self.stdout.write(f'  Orders: {Order.objects.count()}')
        self.stdout.write(f'    - Pending: {Order.objects.filter(status="pending").count()}')
        self.stdout.write(f'    - Confirmed: {Order.objects.filter(status="confirmed").count()}')
        self.stdout.write(f'    - Completed: {Order.objects.filter(status="delivered").count()}')
        
        self.stdout.write('\nTest Credentials:')
        self.stdout.write(self.style.SUCCESS('  Admin: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('  User: testuser / testpass123'))
        
        self.stdout.write('\nNext Steps:')
        self.stdout.write('  1. Start server: python manage.py runserver')
        self.stdout.write('  2. Login to admin: http://localhost:8000/admin/')
        self.stdout.write('  3. Test API: http://localhost:8000/api/docs/')

