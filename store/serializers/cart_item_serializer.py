from rest_framework import serializers
from store.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem model
    """
    product = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(write_only=True, required=False)
    cart = serializers.SerializerMethodField()
    
    def get_product(self, obj):
        """
        Return product data
        Uses lazy import to avoid circular dependency
        """
        from store.serializers import ProductSerializer
        return ProductSerializer(obj.product, context=self.context).data
    
    def get_cart(self, obj):
        """
        Return cart data (minimal to avoid circular dependency)
        Uses a minimal serializer to avoid circular import
        """
        # Create a minimal cart serializer inline to avoid circular dependency
        class MinimalCartSerializer(serializers.ModelSerializer):
            class Meta:
                model = Cart
                fields = ['id', 'session_id', 'created_at', 'updated_at']
                read_only_fields = ['id', 'session_id', 'created_at', 'updated_at']
        
        return MinimalCartSerializer(obj.cart, context=self.context).data

    class Meta:
        model = CartItem
        fields = [
            'id',
            'cart',
            'product',
            'product_id',
            'quantity',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'cart',
                            'product', 'created_at', 'updated_at']

    def validate_quantity(self, value):
        """
        Validate quantity is at least 1
        """
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class CreateCartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a cart item
    """
    cart_id = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(default=1, min_value=1)

    class Meta:
        model = CartItem
        fields = ['cart_id', 'product_id', 'quantity']

    def validate_quantity(self, value):
        """
        Validate quantity is at least 1
        """
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
