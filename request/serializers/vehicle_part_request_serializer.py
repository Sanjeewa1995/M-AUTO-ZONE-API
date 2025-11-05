from rest_framework import serializers
from request.models import VehiclePartRequest
from authentication.serializers import UserSerializer
from store.serializers import ProductSerializer


class VehiclePartRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for VehiclePartRequest model
    """
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = VehiclePartRequest
        fields = [
            'id',
            'vehicle_type',
            'vehicle_model',
            'vehicle_year',
            'part_name',
            'part_number',
            'vehicle_image',
            'part_image',
            'part_video',
            'description',
            'status',
            'user',
            'products',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class VehiclePartRequestCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating vehicle part requests (without user field)
    """
    class Meta:
        model = VehiclePartRequest
        fields = [
            'vehicle_type',
            'vehicle_model',
            'vehicle_year',
            'part_name',
            'part_number',
            'vehicle_image',
            'part_image',
            'part_video',
            'description'
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
                f"Vehicle year must be between 1900 and {current_year + 1}"
            )
        return value


class VehiclePartRequestUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating vehicle part requests
    """
    class Meta:
        model = VehiclePartRequest
        fields = [
            'vehicle_type',
            'vehicle_model',
            'vehicle_year',
            'part_name',
            'part_number',
            'vehicle_image',
            'part_image',
            'part_video',
            'description',
            'status'
        ]
        read_only_fields = ['user']

    def validate_vehicle_year(self, value):
        """
        Validate vehicle year
        """
        from datetime import datetime
        current_year = datetime.now().year

        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(
                f"Vehicle year must be between 1900 and {current_year + 1}"
            )
        return value
