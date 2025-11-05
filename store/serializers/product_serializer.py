from rest_framework import serializers
from store.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image']
        read_only_fields = ['id']
