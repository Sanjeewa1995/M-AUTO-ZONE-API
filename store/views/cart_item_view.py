from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from store.models import CartItem, Cart, Product
from store.serializers import CartItemSerializer, CreateCartItemSerializer
from common.utils import APIResponse


class CartItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CartItem CRUD operations
    
    list: GET /api/v1/store/cart-items/ - List all cart items
    create: POST /api/v1/store/cart-items/ - Create a new cart item
    retrieve: GET /api/v1/store/cart-items/<id>/ - Get a specific cart item
    update: PUT /api/v1/store/cart-items/<id>/ - Update a cart item
    partial_update: PATCH /api/v1/store/cart-items/<id>/ - Partially update a cart item
    destroy: DELETE /api/v1/store/cart-items/<id>/ - Delete a cart item
    """
    queryset = CartItem.objects.select_related('cart', 'product').all()
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]  # Session-based, no authentication required
    
    def get_serializer_class(self):
        """
        Use CreateCartItemSerializer for create action
        """
        if self.action == 'create':
            return CreateCartItemSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        """
        Filter cart items by cart session_id if provided
        """
        queryset = super().get_queryset()
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Create a new cart item
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get cart from cart_id
        cart_id = serializer.validated_data['cart_id']
        cart = get_object_or_404(Cart, id=cart_id)
        
        # Get product
        product_id = serializer.validated_data['product_id']
        product = get_object_or_404(Product, id=product_id)
        
        # Check if cart item already exists for this cart and product
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': serializer.validated_data.get('quantity', 1)}
        )
        
        if not created:
            # If item already exists, update quantity
            cart_item.quantity += serializer.validated_data.get('quantity', 1)
            cart_item.save()
        
        # Return the cart item with full details
        response_serializer = CartItemSerializer(cart_item)
        
        return APIResponse.success(
            data=response_serializer.data,
            message='Cart item added successfully',
            status_code=status.HTTP_201_CREATED
        )
    
    def list(self, request, *args, **kwargs):
        """
        List all cart items
        """
        response = super().list(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Cart items retrieved successfully'
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific cart item
        """
        response = super().retrieve(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Cart item retrieved successfully'
        )
    
    def update(self, request, *args, **kwargs):
        """
        Update a cart item
        """
        response = super().update(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Cart item updated successfully'
        )
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a cart item
        """
        response = super().partial_update(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Cart item updated successfully'
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a cart item
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse.success(
            message='Cart item deleted successfully',
            status_code=status.HTTP_200_OK
        )

