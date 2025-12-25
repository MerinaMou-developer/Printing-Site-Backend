"""
Cart Views with Document Upload Support (JWT Required)
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from apps.cart.models import Cart, CartItem, CartItemDocument
from apps.catalog.models import Product, ProductRequirement
from . import serializers


class CartViewSet(viewsets.ViewSet):
    """
    Cart management with document uploads
    
    GET /api/v1/cart/ - Get user's cart
    POST /api/v1/cart/items/ - Add item to cart
    PATCH /api/v1/cart/items/{item_id}/ - Update cart item quantity
    DELETE /api/v1/cart/items/{item_id}/ - Remove item from cart
    GET /api/v1/cart/items/{item_id}/requirements/ - Get requirements status
    POST /api/v1/cart/items/{item_id}/documents/ - Upload document
    GET /api/v1/cart/items/{item_id}/documents/ - List documents
    DELETE /api/v1/cart/items/{item_id}/documents/{doc_id}/ - Delete document
    """
    permission_classes = []  # Allow both authenticated and guest users
    
    def get_permissions(self):
        """Allow public access for cart operations"""
        return []  # No authentication required
    
    def get_cart(self, request):
        """Get or create cart for user or guest"""
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            # Guest user - use session ID
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            cart, created = Cart.objects.get_or_create(
                session_id=session_id,
                user__isnull=True,
                defaults={'session_id': session_id}
            )
        return cart
    
    def list(self, request):
        """Get user's or guest's cart"""
        cart = self.get_cart(request)
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='items')
    def add_item(self, request):
        """
        Add item to cart with optional document uploads
        Works for both authenticated and guest users
        
        Accepts:
        - product_id (required)
        - quantity (optional, default: 1)
        - emirates_id (optional file)
        - trade_license (optional file)
        - design (optional file)
        
        Can be sent as:
        - JSON: {"product_id": 1, "quantity": 4}
        - multipart/form-data: product_id=1&quantity=4&emirates_id=<file>&trade_license=<file>&design=<file>
        """
        serializer = serializers.AddCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cart = self.get_cart(request)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data.get('quantity', 1)
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Check if item already exists
        cart_item = CartItem.objects.filter(
            cart=cart,
            product=product
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
        
        # Handle document uploads if provided
        uploaded_documents = []
        errors = []
        
        # Upload Emirates ID if provided
        if serializer.validated_data.get('emirates_id'):
            try:
                # Delete existing document of this type
                CartItemDocument.objects.filter(
                    cart_item=cart_item,
                    doc_type='EMIRATES_ID'
                ).delete()
                
                # Create new document
                document = CartItemDocument.objects.create(
                    cart_item=cart_item,
                    doc_type='EMIRATES_ID',
                    file=serializer.validated_data['emirates_id'],
                    file_name=serializer.validated_data['emirates_id'].name,
                    file_size=serializer.validated_data['emirates_id'].size
                )
                uploaded_documents.append(serializers.CartItemDocumentSerializer(document).data)
            except Exception as e:
                errors.append(f'Failed to upload Emirates ID: {str(e)}')
        
        # Upload Trade License if provided
        if serializer.validated_data.get('trade_license'):
            try:
                # Delete existing document of this type
                CartItemDocument.objects.filter(
                    cart_item=cart_item,
                    doc_type='TRADE_LICENSE'
                ).delete()
                
                # Create new document
                document = CartItemDocument.objects.create(
                    cart_item=cart_item,
                    doc_type='TRADE_LICENSE',
                    file=serializer.validated_data['trade_license'],
                    file_name=serializer.validated_data['trade_license'].name,
                    file_size=serializer.validated_data['trade_license'].size
                )
                uploaded_documents.append(serializers.CartItemDocumentSerializer(document).data)
            except Exception as e:
                errors.append(f'Failed to upload Trade License: {str(e)}')
        
        # Upload Design if provided
        if serializer.validated_data.get('design'):
            try:
                # Delete existing document of this type
                CartItemDocument.objects.filter(
                    cart_item=cart_item,
                    doc_type='DESIGN'
                ).delete()
                
                # Create new document
                document = CartItemDocument.objects.create(
                    cart_item=cart_item,
                    doc_type='DESIGN',
                    file=serializer.validated_data['design'],
                    file_name=serializer.validated_data['design'].name,
                    file_size=serializer.validated_data['design'].size
                )
                uploaded_documents.append(serializers.CartItemDocumentSerializer(document).data)
            except Exception as e:
                errors.append(f'Failed to upload Design: {str(e)}')
        
        # Refresh cart to get updated data
        cart.refresh_from_db()
        cart_serializer = serializers.CartSerializer(cart)
        
        response_data = {
            'message': 'Item added to cart successfully!',
            'cart': cart_serializer.data
        }
        
        if uploaded_documents:
            response_data['uploaded_documents'] = uploaded_documents
            response_data['message'] += f' {len(uploaded_documents)} document(s) uploaded.'
        
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['patch', 'put'], url_path='items/(?P<item_id>[^/.]+)')
    def update_item(self, request, item_id=None):
        """Update cart item quantity"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        serializer = serializers.UpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = serializer.validated_data['quantity']
        cart_item.save()
        
        cart_serializer = serializers.CartSerializer(cart)
        return Response({
            'message': 'Cart item updated successfully!',
            'cart': cart_serializer.data
        })
    
    @action(detail=False, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def remove_item(self, request, item_id=None):
        """Remove item from cart"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        cart_serializer = serializers.CartSerializer(cart)
        return Response({
            'message': 'Item removed from cart successfully!',
            'cart': cart_serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='items/(?P<item_id>[^/.]+)/requirements')
    def get_requirements(self, request, item_id=None):
        """Get requirements status for cart item"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        # Get product requirements
        requirements = ProductRequirement.objects.filter(product=cart_item.product)
        
        # Get uploaded documents
        uploaded_docs = CartItemDocument.objects.filter(cart_item=cart_item)
        uploaded_types = set(uploaded_docs.values_list('doc_type', flat=True))
        
        # Build requirements status
        requirements_status = []
        for req in requirements:
            requirements_status.append({
                'doc_type': req.doc_type,
                'doc_type_display': req.get_doc_type_display(),
                'is_required': req.is_required,
                'description': req.description,
                'is_uploaded': req.doc_type in uploaded_types,
                'uploaded_document': serializers.CartItemDocumentSerializer(
                    uploaded_docs.filter(doc_type=req.doc_type).first()
                ).data if req.doc_type in uploaded_types else None
            })
        
        return Response({
            'cart_item_id': cart_item.id,
            'product_id': cart_item.product.id,
            'product_name': cart_item.product.name,
            'requirements': requirements_status,
            'all_required_uploaded': all(
                req['is_uploaded'] for req in requirements_status if req['is_required']
            )
        })
    
    @action(detail=False, methods=['post'], url_path='items/(?P<item_id>[^/.]+)/documents')
    def upload_document(self, request, item_id=None):
        """Upload document for cart item (allows upload even if requirement not set)"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        serializer = serializers.UploadDocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        doc_type = serializer.validated_data['doc_type']
        file = serializer.validated_data['file']
        
        # Allow upload even if requirement not set (better UX)
        # Requirements will be validated at checkout
        
        # Delete existing document of this type
        CartItemDocument.objects.filter(cart_item=cart_item, doc_type=doc_type).delete()
        
        # Create new document
        document = CartItemDocument.objects.create(
            cart_item=cart_item,
            doc_type=doc_type,
            file=file,
            file_name=file.name,
            file_size=file.size
        )
        
        return Response(
            serializers.CartItemDocumentSerializer(document).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'], url_path='items/(?P<item_id>[^/.]+)/documents')
    def list_documents(self, request, item_id=None):
        """List all documents for cart item"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        documents = CartItemDocument.objects.filter(cart_item=cart_item)
        serializer = serializers.CartItemDocumentSerializer(documents, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)/documents/(?P<doc_id>[^/.]+)')
    def delete_document(self, request, item_id=None, doc_id=None):
        """Delete document"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        document = get_object_or_404(CartItemDocument, id=doc_id, cart_item=cart_item)
        
        document.delete()
        return Response(
            {'message': 'Document deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['post'], url_path='items/(?P<item_id>[^/.]+)/documents/bulk')
    def bulk_upload_documents(self, request, item_id=None):
        """Upload all documents at once for a cart item"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        serializer = serializers.BulkUploadDocumentsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_documents = []
        errors = []
        
        # Upload Emirates ID
        if serializer.validated_data.get('emirates_id'):
            try:
                # Delete existing document
                CartItemDocument.objects.filter(
                    cart_item=cart_item, 
                    doc_type='EMIRATES_ID'
                ).delete()
                
                # Create new document (allow upload even if requirement not set)
                document = CartItemDocument.objects.create(
                    cart_item=cart_item,
                    doc_type='EMIRATES_ID',
                    file=serializer.validated_data['emirates_id'],
                    file_name=serializer.validated_data['emirates_id'].name,
                    file_size=serializer.validated_data['emirates_id'].size
                )
                uploaded_documents.append(serializers.CartItemDocumentSerializer(document).data)
            except Exception as e:
                errors.append(f'Failed to upload Emirates ID: {str(e)}')
        
        # Upload Trade License
        if serializer.validated_data.get('trade_license'):
            try:
                # Delete existing document
                CartItemDocument.objects.filter(
                    cart_item=cart_item, 
                    doc_type='TRADE_LICENSE'
                ).delete()
                
                # Create new document (allow upload even if requirement not set)
                document = CartItemDocument.objects.create(
                    cart_item=cart_item,
                    doc_type='TRADE_LICENSE',
                    file=serializer.validated_data['trade_license'],
                    file_name=serializer.validated_data['trade_license'].name,
                    file_size=serializer.validated_data['trade_license'].size
                )
                uploaded_documents.append(serializers.CartItemDocumentSerializer(document).data)
            except Exception as e:
                errors.append(f'Failed to upload Trade License: {str(e)}')
        
        # Upload Design (optional - always allowed)
        if serializer.validated_data.get('design'):
            try:
                # Delete existing document
                CartItemDocument.objects.filter(
                    cart_item=cart_item, 
                    doc_type='DESIGN'
                ).delete()
                
                # Create new document (design is always optional)
                document = CartItemDocument.objects.create(
                    cart_item=cart_item,
                    doc_type='DESIGN',
                    file=serializer.validated_data['design'],
                    file_name=serializer.validated_data['design'].name,
                    file_size=serializer.validated_data['design'].size
                )
                uploaded_documents.append(serializers.CartItemDocumentSerializer(document).data)
            except Exception as e:
                errors.append(f'Failed to upload Design: {str(e)}')
        
        response_data = {
            'message': f'Uploaded {len(uploaded_documents)} document(s)',
            'uploaded_documents': uploaded_documents
        }
        
        if errors:
            response_data['errors'] = errors
        
        status_code = status.HTTP_201_CREATED if uploaded_documents else status.HTTP_400_BAD_REQUEST
        return Response(response_data, status=status_code)

