from rest_framework import serializers
from store.models import Cart
from decimal import Decimal
from django.db.models import Sum, F


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart model
    """
    items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'session_id',
            'items',
            'total',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'session_id', 'created_at', 'updated_at']
    
    def get_items(self, obj):
        """
        Return cart items for this cart
        Uses lazy import to avoid circular dependency
        """
        from store.serializers import CartItemSerializer
        items = obj.items.all()
        return CartItemSerializer(items, many=True, context=self.context).data
    
    def get_total(self, obj):
        """
        Calculate the total price of all items in the cart
        Total = sum(product.price * quantity) for all items
        Uses database aggregation for better performance
        """
        from store.models import CartItem
        
        total = CartItem.objects.filter(cart=obj).aggregate(
            total=Sum(F('product__price') * F('quantity'))
        )['total']
        
        # Return '0.00' if cart is empty, otherwise return the total as string
        return str(total) if total else '0.00'


class CreateCartSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new cart
    Session ID is auto-generated, so no fields needed
    """
    class Meta:
        model = Cart
        fields = []  # No fields needed, session_id is auto-generated
