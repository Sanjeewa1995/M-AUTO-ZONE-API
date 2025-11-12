from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny
from store.models import Order
from store.serializers import OrderSerializer, CreateOrderSerializer
from common.utils import APIResponse


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Order model
    Supports create and retrieve operations
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        """
        Use CreateOrderSerializer for create action
        """
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new order
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Return the created order with full details
        response_serializer = OrderSerializer(order, context={'request': request})
        
        return APIResponse.success(
            data=response_serializer.data,
            message='Order created successfully',
            status_code=status.HTTP_201_CREATED
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific order
        """
        response = super().retrieve(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Order retrieved successfully'
        )

