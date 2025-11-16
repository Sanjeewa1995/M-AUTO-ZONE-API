from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from store.models import Order
from store.serializers import OrderSerializer, CreateOrderSerializer
from common.utils import APIResponse, CustomPageNumberPagination


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Order model
    Supports create, retrieve, and list operations
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        """
        Filter orders by authenticated user for list action
        """
        queryset = super().get_queryset()
        if self.action == 'list' and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset.select_related('user', 'shipping_address', 'cart').prefetch_related('items__product')
    
    def get_serializer_class(self):
        """
        Use CreateOrderSerializer for create action
        """
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer
    
    def get_permissions(self):
        """
        Require authentication for list and create actions, allow any for retrieve
        """
        if self.action in ['list', 'create']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
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
    
    def list(self, request, *args, **kwargs):
        """
        List orders for the authenticated user
        """
        response = super().list(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Orders retrieved successfully'
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

