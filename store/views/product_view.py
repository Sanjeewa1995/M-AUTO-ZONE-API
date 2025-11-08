from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from store.models import Product
from store.serializers import ProductSerializer
from common.utils import CustomPageNumberPagination, APIResponse


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Product read operations only
    
    list: GET /api/v1/store/products/ - List all products
    retrieve: GET /api/v1/store/products/<id>/ - Get a specific product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['request']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'price']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return the queryset of products for the authenticated user
        """
        return Product.objects.select_related('request').filter(request__user=self.request.user)
    
    def get_serializer_context(self):
        """
        Add request to serializer context for building absolute URLs
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def list(self, request, *args, **kwargs):
        """
        List all products
        """
        response = super().list(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Products retrieved successfully'
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific product
        """
        response = super().retrieve(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data,
            message='Product retrieved successfully'
        )

