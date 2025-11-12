from rest_framework import serializers
from store.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for Address model
    """
    class Meta:
        model = Address
        fields = [
            'id',
            'first_name',
            'last_name',
            'country',
            'state',
            'post_code',
            'city',
            'address1',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CreateAddressSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an address
    """
    class Meta:
        model = Address
        fields = [
            'first_name',
            'last_name',
            'country',
            'state',
            'post_code',
            'city',
            'address1'
        ]

