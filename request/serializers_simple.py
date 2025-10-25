from rest_framework import serializers
from .models import VehiclePartRequest
from authentication.serializers import UserSerializer

class VehiclePartRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for vehicle part requests
    """
    user = UserSerializer(read_only=True)
    vehicle_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = VehiclePartRequest
        fields = [
            'id', 'vehicle_type', 'vehicle_model', 'vehicle_year',
            'part_name', 'part_number', 'vehicle_image', 'part_image',
            'part_video', 'description', 'status', 'user',
            'vehicle_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class VehiclePartRequestCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating vehicle part requests (without user field)
    """
    class Meta:
        model = VehiclePartRequest
        fields = [
            'vehicle_type', 'vehicle_model', 'vehicle_year',
            'part_name', 'part_number', 'vehicle_image', 'part_image',
            'part_video', 'description'
        ]
    
    def create(self, validated_data):
        """
        Create a new vehicle part request
        """
        # Set the user from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_vehicle_year(self, value):
        """
        Validate vehicle year
        """
        from datetime import datetime
        current_year = datetime.now().year
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(
                f'Vehicle year must be between 1900 and {current_year + 1}'
            )
        return value

class VehiclePartRequestUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating vehicle part requests
    """
    class Meta:
        model = VehiclePartRequest
        fields = [
            'vehicle_type', 'vehicle_model', 'vehicle_year',
            'part_name', 'part_number', 'vehicle_image', 'part_image',
            'part_video', 'description', 'status'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def validate_vehicle_year(self, value):
        """
        Validate vehicle year
        """
        from datetime import datetime
        current_year = datetime.now().year
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(
                f'Vehicle year must be between 1900 and {current_year + 1}'
            )
        return value
