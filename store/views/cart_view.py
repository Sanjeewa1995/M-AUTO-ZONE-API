from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny
from store.models import Cart
from store.serializers import CartSerializer, CreateCartSerializer
from common.utils import APIResponse


class CartViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    """
    ViewSet for Cart model
    """
    queryset = Cart.objects.all()
    serializer_class = CreateCartSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        """
        Use CreateCartSerializer for create action
        """
        if self.action == 'create':
            return CreateCartSerializer
        return CartSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new cart with auto-generated session_id
        """
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()

        # Return the created cart with full details
        response_serializer = CartSerializer(cart)

        return APIResponse.success(
            data=response_serializer.data,
            message='Cart created successfully',
            status_code=status.HTTP_201_CREATED
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific cart
        """
        response = super().retrieve(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Cart retrieved successfully'
        )
    
    def update(self, request, *args, **kwargs):
        """
        Update a cart
        """
        response = super().update(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Cart updated successfully'
        )
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a cart
        """
        response = super().partial_update(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Cart updated successfully'
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a cart
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse.success(
            message='Cart deleted successfully',
            status_code=status.HTTP_200_OK
        )
