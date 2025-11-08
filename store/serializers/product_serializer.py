from rest_framework import serializers
from store.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model
    """
    request = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image',
            'request',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_request(self, obj):
        """
        Return the request data for this product
        Uses a minimal serializer to avoid infinite recursion (products -> request -> products)
        """
        if obj.request:
            # Use a minimal serializer that doesn't include products to avoid recursion
            from rest_framework import serializers
            # Create a minimal request serializer inline to avoid circular imports
            class MinimalRequestSerializer(serializers.ModelSerializer):

                class Meta:
                    from request.models import VehiclePartRequest
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
                        'created_at',
                        'updated_at'
                    ]
                    read_only_fields = ['id', 'created_at', 'updated_at']

            return MinimalRequestSerializer(obj.request, context=self.context).data
        return None
