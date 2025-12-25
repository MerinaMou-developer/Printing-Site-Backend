"""
Order Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from django.db import transaction

from apps.orders.models import Order, OrderItem, OrderDocument
from apps.cart.models import Cart
from . import serializers


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
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        """Users see only their orders, admins see all"""
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Order.objects.all().prefetch_related('items', 'documents')
        return Order.objects.filter(user=self.request.user).prefetch_related('items', 'documents')
    
    def get_serializer_class(self):
        """Use appropriate serializer based on action"""
        if self.action == 'list':
            return serializers.OrderListSerializer
        elif self.action == 'create':
            return serializers.OrderCreateSerializer
        elif self.action == 'checkout':
            return serializers.CheckoutSerializer
        return serializers.OrderDetailSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new order"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                serializers.OrderDetailSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[])
    @transaction.atomic
    def checkout(self, request):
        """
        Create order from cart with document validation
        Works for both authenticated and guest users
        
        For authenticated users: Finds cart by user
        For guest users: Finds cart by session_id
        
        Validates:
        - Cart exists and has items
        - All required documents are uploaded for each product
        - Safely copies all documents from cart to order
        """
        # Validate checkout data
        checkout_serializer = serializers.CheckoutSerializer(data=request.data)
        if not checkout_serializer.is_valid():
            return Response(checkout_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get cart - support both authenticated and guest users
        try:
            if request.user.is_authenticated:
                # Authenticated user - find cart by user
                cart = Cart.objects.select_related('user').prefetch_related(
                    'items__product',
                    'items__variant',
                    'items__documents'
                ).get(user=request.user)
            else:
                # Guest user - find cart by session_id
                session_id = request.session.session_key
                if not session_id:
                    return Response(
                        {'error': 'Session not found. Please add items to cart first.'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                cart = Cart.objects.prefetch_related(
                    'items__product',
                    'items__variant',
                    'items__documents'
                ).get(session_id=session_id, user__isnull=True)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart not found. Please add items to cart first.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Validate cart has items
        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate required documents for all cart items
        # Check based on product category (stamp products need documents)
        missing_documents = []
        
        # Stamp categories that require documents
        stamp_category_slugs = [
            'dater-stamp-products',
            'handy-and-pocket-stamps',
            'heavy-duty-stamps',
            'oval-self-ink-stamps',
            'round-self-ink-stamps'
        ]
        
        for cart_item in cart.items.all():
            product = cart_item.product
            
            # Check if product is in a stamp category
            is_stamp_product = (
                product.category and 
                product.category.slug in stamp_category_slugs
            )
            
            if is_stamp_product:
                # Get uploaded documents for this cart item
                uploaded_doc_types = set(
                    cart_item.documents.values_list('doc_type', flat=True)
                )
                
                # Required documents for stamp products
                required_docs = ['EMIRATES_ID', 'TRADE_LICENSE']
                doc_display_names = {
                    'EMIRATES_ID': 'Emirates ID',
                    'TRADE_LICENSE': 'Trade License'
                }
                
                # Check for missing required documents
                for doc_type in required_docs:
                    if doc_type not in uploaded_doc_types:
                        missing_documents.append({
                            'product_id': product.id,
                            'product_name': product.name,
                            'missing_document': doc_display_names[doc_type],
                            'doc_type': doc_type
                        })
        
        if missing_documents:
            return Response(
                {
                    'error': 'Missing required documents',
                    'missing_documents': missing_documents,
                    'message': 'Please upload all required documents before checkout'
                },
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
            user=request.user if request.user.is_authenticated else None,  # Guest orders have user=None
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
        
        # Create order items from cart items and safely copy documents
        for cart_item in cart.items.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                variant=cart_item.variant,
                variant_name=cart_item.variant.name if cart_item.variant else None,
                quantity=cart_item.quantity,
                price=cart_item.price,
            )
            
            # Safely copy all documents from cart item to order
            for cart_doc in cart_item.documents.all():
                try:
                    OrderDocument.objects.create(
                        order=order,
                        order_item=order_item,
                        doc_type=cart_doc.doc_type,
                        file=cart_doc.file,  # Django handles file copying
                        file_name=cart_doc.file_name,
                        file_size=cart_doc.file_size,
                        product_name=cart_item.product.name
                    )
                except Exception as e:
                    # If document copy fails, rollback transaction
                    raise Exception(f"Failed to copy document {cart_doc.file_name}: {str(e)}")
        
        # Clear cart after successful order creation
        cart.items.all().delete()
        
        return Response(
            serializers.OrderDetailSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def update_status(self, request, id=None):
        """Update order status (admin only)"""
        order = self.get_object()
        serializer = serializers.OrderStatusUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        new_status = serializer.validated_data['status']
        old_status = order.status
        order.status = new_status
        
        # Update timestamps based on status
        if new_status == 'confirmed' and not order.confirmed_at:
            order.confirmed_at = timezone.now()
        elif new_status == 'shipped' and not order.shipped_at:
            order.shipped_at = timezone.now()
        elif new_status == 'delivered' and not order.delivered_at:
            order.delivered_at = timezone.now()
        
        # Save order - the model's save() method will automatically update
        # product sold counts if status changed to/from 'delivered'
        order.save()
        
        return Response({
            'message': f'Order status updated from {old_status} to {new_status}',
            'order': serializers.OrderDetailSerializer(order).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def update_payment_status(self, request, id=None):
        """Update payment status (admin only)"""
        order = self.get_object()
        serializer = serializers.PaymentStatusUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        new_payment_status = serializer.validated_data['payment_status']
        old_payment_status = order.payment_status
        order.payment_status = new_payment_status
        order.save()
        
        return Response({
            'message': f'Payment status updated from {old_payment_status} to {new_payment_status}',
            'order': serializers.OrderDetailSerializer(order).data
        })

