from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q, Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Category, Product, ProductImage, ProductSpecification, ProductVariant,
    Cart, CartItem, Order, OrderItem, OrderFile
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserUpdateSerializer, ChangePasswordSerializer,
    EmailOnlyTokenObtainPairSerializer,
    CategorySerializer, CategoryListSerializer,
    ProductListSerializer, ProductDetailSerializer,
    ProductImageSerializer, ProductSpecificationSerializer, ProductVariantSerializer,
    CartSerializer, CartItemSerializer, AddToCartSerializer, UpdateCartItemSerializer,
    OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer, CheckoutSerializer,
    OrderStatusUpdateSerializer, PaymentStatusUpdateSerializer, OrderFileSerializer
)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailOnlyTokenObtainPairSerializer

User = get_user_model()


# ============ Authentication Views ============

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully!'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """Update user profile"""
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'user': UserSerializer(request.user).data,
            'message': 'Profile updated successfully!'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password"""
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': ['Wrong password.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully!'
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============ Category ViewSet ============

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product categories
    
    list: Get all categories
    retrieve: Get single category
    create: Create new category (admin only)
    update: Update category (admin only)
    destroy: Delete category (admin only)
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order', 'created_at']
    ordering = ['order', 'name']
    
    def get_permissions(self):
        """Allow read-only access to everyone, write access to admins only"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Use simplified serializer for lists"""
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer
    
    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """Get all products in a category"""
        category = self.get_object()
        products = Product.objects.filter(category=category, is_active=True)
        
        # Apply filters
        search = request.query_params.get('search', None)
        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        # Pagination
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


# ============ Product ViewSet ============

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products
    
    list: Get all products with filtering and search
    retrieve: Get single product with all details
    create: Create new product (admin only)
    update: Update product (admin only)
    destroy: Delete product (admin only)
    featured: Get featured products
    search: Search products
    """
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related(
        'images', 'specifications', 'variants'
    )
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'in_stock']
    search_fields = ['name', 'description', 'short_description', 'sku']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Allow read-only access to everyone, write access to admins only"""
        if self.action in ['list', 'retrieve', 'featured', 'search']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Use simplified serializer for lists"""
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products"""
        products = self.queryset.filter(is_featured=True)[:8]
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced product search"""
        query = request.query_params.get('q', '')
        category_slug = request.query_params.get('category', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        in_stock = request.query_params.get('in_stock', None)
        
        products = self.queryset
        
        # Text search
        if query:
            products = products.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(short_description__icontains=query) |
                Q(sku__icontains=query)
            )
        
        # Category filter
        if category_slug:
            products = products.filter(category__slug=category_slug)
        
        # Price filters
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        
        # Stock filter
        if in_stock == 'true':
            products = products.filter(in_stock=True)
        
        # Pagination
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


# ============ Cart ViewSet ============

class CartViewSet(viewsets.ViewSet):
    """
    ViewSet for managing shopping cart
    
    list: Get current user's cart (same as retrieve)
    retrieve: Get current user's cart
    add_item: Add item to cart
    update_item: Update cart item quantity
    remove_item: Remove item from cart
    clear: Clear entire cart
    """
    permission_classes = [IsAuthenticated]
    
    def get_cart(self, user):
        """Get or create cart for user"""
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    
    def list(self, request):
        """Get user's cart (for standard REST access)"""
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Get user's cart (alternative access)"""
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cart = self.get_cart(request.user)
        product_id = serializer.validated_data['product_id']
        variant_id = serializer.validated_data.get('variant_id')
        quantity = serializer.validated_data['quantity']
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        variant = None
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id, product=product, is_active=True)
        
        # Check if item already exists in cart
        cart_item = CartItem.objects.filter(
            cart=cart,
            product=product,
            variant=variant
        ).first()
        
        if cart_item:
            # Update quantity
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # Create new cart item
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                variant=variant,
                quantity=quantity
            )
        
        # Return updated cart
        cart_serializer = CartSerializer(cart)
        return Response({
            'message': 'Item added to cart successfully!',
            'cart': cart_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['put', 'patch'], url_path='items/(?P<item_id>[^/.]+)')
    def update_item(self, request, item_id=None):
        """Update cart item quantity"""
        cart = self.get_cart(request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        serializer = UpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = serializer.validated_data['quantity']
        cart_item.save()
        
        # Return updated cart
        cart_serializer = CartSerializer(cart)
        return Response({
            'message': 'Cart item updated successfully!',
            'cart': cart_serializer.data
        })
    
    @action(detail=False, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def remove_item(self, request, item_id=None):
        """Remove item from cart"""
        cart = self.get_cart(request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        # Return updated cart
        cart_serializer = CartSerializer(cart)
        return Response({
            'message': 'Item removed from cart successfully!',
            'cart': cart_serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear all items from cart"""
        cart = self.get_cart(request.user)
        cart.items.all().delete()
        
        # Return empty cart
        cart_serializer = CartSerializer(cart)
        return Response({
            'message': 'Cart cleared successfully!',
            'cart': cart_serializer.data
        })


# ============ Order ViewSet ============

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders
    
    list: Get user's orders (or all orders for admin)
    retrieve: Get single order
    create: Create new order
    checkout: Create order from cart
    update_status: Update order status (admin only)
    update_payment_status: Update payment status (admin only)
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status']
    search_fields = ['order_number', 'first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['created_at', 'total', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Users see only their orders, admins see all"""
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Order.objects.all().prefetch_related('items', 'files')
        return Order.objects.filter(user=self.request.user).prefetch_related('items', 'files')
    
    def get_serializer_class(self):
        """Use appropriate serializer based on action"""
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'checkout':
            return CheckoutSerializer
        return OrderDetailSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new order"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                OrderDetailSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Create order from user's cart"""
        # Validate checkout data
        checkout_serializer = CheckoutSerializer(data=request.data)
        if not checkout_serializer.is_valid():
            return Response(checkout_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Validate cart has items
        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate totals
        subtotal = cart.subtotal
        shipping_cost = 0  # Calculate based on your business logic
        tax = 0  # Calculate based on your business logic
        total = subtotal + shipping_cost + tax
        
        # Create order
        validated_data = checkout_serializer.validated_data
        order = Order.objects.create(
            user=request.user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            company_name=validated_data.get('company_name', ''),
            address_line_1=validated_data['address_line_1'],
            address_line_2=validated_data.get('address_line_2', ''),
            city=validated_data['city'],
            state=validated_data.get('state', ''),
            country=validated_data['country'],
            postal_code=validated_data.get('postal_code', ''),
            order_notes=validated_data.get('order_notes', ''),
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            total=total,
            status='pending',
            payment_status='pending'
        )
        
        # Create order items from cart items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                variant=cart_item.variant,
                variant_name=cart_item.variant.name if cart_item.variant else None,
                quantity=cart_item.quantity,
                price=cart_item.price,
            )
        
        # Handle file uploads if provided
        files = request.FILES
        for key, file in files.items():
            # Parse file key: products[0][emiratesId], products[0][tradeLicense], etc.
            if '[' in key and ']' in key:
                try:
                    parts = key.split('[')
                    index = int(parts[1].split(']')[0])
                    file_type = parts[2].rstrip(']')
                    
                    # Get corresponding cart item
                    cart_items_list = list(cart.items.all())
                    if index < len(cart_items_list):
                        cart_item = cart_items_list[index]
                        
                        OrderFile.objects.create(
                            order=order,
                            file=file,
                            file_name=file.name,
                            file_type=file_type,
                            file_size=file.size,
                            product_name=cart_item.product.name
                        )
                except (ValueError, IndexError):
                    pass
        
        # Clear cart after successful order
        cart.items.all().delete()
        
        return Response(
            OrderDetailSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        """Update order status (admin only)"""
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        new_status = serializer.validated_data['status']
        old_status = order.status
        order.status = new_status
        
        # Update timestamps based on status
        from django.utils import timezone
        if new_status == 'confirmed' and not order.confirmed_at:
            order.confirmed_at = timezone.now()
        elif new_status == 'shipped' and not order.shipped_at:
            order.shipped_at = timezone.now()
        elif new_status == 'delivered' and not order.delivered_at:
            order.delivered_at = timezone.now()
        
        order.save()
        
        return Response({
            'message': f'Order status updated from {old_status} to {new_status}',
            'order': OrderDetailSerializer(order).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def update_payment_status(self, request, pk=None):
        """Update payment status (admin only)"""
        order = self.get_object()
        serializer = PaymentStatusUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        new_payment_status = serializer.validated_data['payment_status']
        old_payment_status = order.payment_status
        order.payment_status = new_payment_status
        order.save()
        
        return Response({
            'message': f'Payment status updated from {old_payment_status} to {new_payment_status}',
            'order': OrderDetailSerializer(order).data
        })


# ============ Product Related ViewSets ============

class ProductImageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing product images (admin only)"""
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']


class ProductSpecificationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing product specifications (admin only)"""
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']


class ProductVariantViewSet(viewsets.ModelViewSet):
    """ViewSet for managing product variants (admin only)"""
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'is_active']


# ============ Statistics View (Admin) ============

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_statistics(request):
    """Get admin dashboard statistics"""
    from django.db.models import Sum, Count, Avg
    from datetime import timedelta
    from django.utils import timezone
    
    # Date ranges
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    
    # Orders statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='delivered').count()
    
    # Revenue statistics
    total_revenue = Order.objects.filter(
        payment_status='paid'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    revenue_30_days = Order.objects.filter(
        payment_status='paid',
        created_at__date__gte=last_30_days
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Products statistics
    total_products = Product.objects.filter(is_active=True).count()
    out_of_stock = Product.objects.filter(is_active=True, in_stock=False).count()
    
    # Users statistics
    total_users = User.objects.count()
    new_users_30_days = User.objects.filter(
        date_joined__date__gte=last_30_days
    ).count()
    
    # Recent orders
    recent_orders = Order.objects.all()[:10]
    recent_orders_data = OrderListSerializer(recent_orders, many=True).data
    
    return Response({
        'orders': {
            'total': total_orders,
            'pending': pending_orders,
            'completed': completed_orders,
        },
        'revenue': {
            'total': float(total_revenue),
            'last_30_days': float(revenue_30_days),
        },
        'products': {
            'total': total_products,
            'out_of_stock': out_of_stock,
        },
        'users': {
            'total': total_users,
            'new_last_30_days': new_users_30_days,
        },
        'recent_orders': recent_orders_data,
    })
