from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import VehiclePartRequest
from .serializers import (
    VehiclePartRequestSerializer,
    VehiclePartRequestCreateSerializer,
    VehiclePartRequestUpdateSerializer
)
from authentication.utils import APIResponse


class VehiclePartRequestListCreateView(generics.ListCreateAPIView):
    """
    List all vehicle part requests or create a new one
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vehicle_type', 'status', 'vehicle_year']
    search_fields = ['vehicle_model', 'part_name', 'part_number', 'description']
    ordering_fields = ['created_at', 'updated_at', 'vehicle_year']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VehiclePartRequestCreateSerializer
        return VehiclePartRequestSerializer
    
    def get_queryset(self):
        """
        Return requests for the authenticated user
        """
        return VehiclePartRequest.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return APIResponse.validation_error(serializer.errors)
        
        vehicle_part_request = serializer.save()
        
        # Return the created object with full details
        response_serializer = VehiclePartRequestSerializer(vehicle_part_request)
        
        return APIResponse.success(
            data=response_serializer.data,
            message='Vehicle part request created successfully',
            status_code=status.HTTP_201_CREATED
        )


class VehiclePartRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a vehicle part request
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return VehiclePartRequestUpdateSerializer
        return VehiclePartRequestSerializer
    
    def get_queryset(self):
        """
        Return requests for the authenticated user
        """
        return VehiclePartRequest.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return APIResponse.validation_error(serializer.errors)
        
        vehicle_part_request = serializer.save()
        
        # Return the updated object with full details
        response_serializer = VehiclePartRequestSerializer(vehicle_part_request)
        
        return APIResponse.success(
            data=response_serializer.data,
            message='Vehicle part request updated successfully'
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return APIResponse.success(
            message='Vehicle part request deleted successfully'
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vehicle_part_request_stats_view(request):
    """
    Get statistics for vehicle part requests
    """
    user_requests = VehiclePartRequest.objects.filter(user=request.user)
    
    stats = {
        'total_requests': user_requests.count(),
        'pending_requests': user_requests.filter(status='pending').count(),
        'in_progress_requests': user_requests.filter(status='in_progress').count(),
        'completed_requests': user_requests.filter(status='completed').count(),
        'cancelled_requests': user_requests.filter(status='cancelled').count(),
    }
    
    return APIResponse.success(
        data=stats,
        message='Statistics retrieved successfully'
    )
