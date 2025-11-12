from rest_framework import serializers
from store.models import Order, OrderHasItems, Address
from decimal import Decimal
import uuid


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderHasItems (order items)
    """
    product = serializers.SerializerMethodField()
    
    def get_product(self, obj):
        """
        Return product data
        Uses lazy import to avoid circular dependency
        """
        from store.serializers import ProductSerializer
        return ProductSerializer(obj.product, context=self.context).data
    
    class Meta:
        model = OrderHasItems
        fields = [
            'id',
            'product',
            'price',
            'currency',
            'quantity',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model (read)
    """
    shipping_address = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    cart = serializers.SerializerMethodField()
    cart_id = serializers.IntegerField(source='cart.id', read_only=True, allow_null=True)
    
    def get_shipping_address(self, obj):
        """
        Return shipping address data
        Uses lazy import to avoid circular dependency
        """
        from store.serializers import AddressSerializer
        return AddressSerializer(obj.shipping_address, context=self.context).data
    
    def get_items(self, obj):
        """
        Return order items for this order
        """
        items = obj.items.all()
        return OrderItemSerializer(items, many=True, context=self.context).data
    
    def get_cart(self, obj):
        """
        Return cart data (minimal to avoid circular dependency)
        """
        if not obj.cart:
            return None
        
        from store.serializers import CartSerializer
        return CartSerializer(obj.cart, context=self.context).data
    
    class Meta:
        model = Order
        fields = [
            'id',
            'total',
            'currency',
            'reference_number',
            'source',
            'status',
            'shipping_address',
            'cart',
            'cart_id',
            'items',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'reference_number', 'status', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    """
    Serializer for creating an order from a cart
    Requires cart_id to create order from cart items
    """
    cart_id = serializers.IntegerField(required=True)
    shipping_address = serializers.DictField(required=True)
    source = serializers.ChoiceField(
        choices=['web', 'android', 'ios'],
        required=True
    )
    currency = serializers.CharField(max_length=3, default='LKR', required=False)
    
    def validate_cart_id(self, value):
        """
        Validate that cart exists and has items
        """
        from store.models import Cart, CartItem
        
        try:
            cart = Cart.objects.get(id=value)
        except Cart.DoesNotExist:
            raise serializers.ValidationError(f"Cart with id {value} not found.")
        
        # Check if cart has items
        cart_items_count = CartItem.objects.filter(cart=cart).count()
        if cart_items_count == 0:
            raise serializers.ValidationError("Cart is empty. Cannot create order from empty cart.")
        
        return value
    
    def create(self, validated_data):
        """
        Create order and order items from cart
        """
        from store.models import Cart, CartItem, Product
        
        shipping_address_data = validated_data.pop('shipping_address')
        source = validated_data.get('source')
        currency = validated_data.get('currency', 'LKR')
        cart_id = validated_data.get('cart_id')
        
        # Create shipping address
        from store.serializers import CreateAddressSerializer
        address_serializer = CreateAddressSerializer(data=shipping_address_data)
        address_serializer.is_valid(raise_exception=True)
        shipping_address = address_serializer.save()
        
        # Get cart and cart items
        cart = Cart.objects.get(id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        
        if not cart_items.exists():
            raise serializers.ValidationError("Cart is empty. Cannot create order from empty cart.")
        
        # Calculate total and create order items
        total = Decimal('0.00')
        order_items_to_create = []
        
        for cart_item in cart_items:
            product = cart_item.product
            quantity = cart_item.quantity
            
            item_total = product.price * Decimal(str(quantity))
            total += item_total
            
            order_items_to_create.append({
                'product': product,
                'price': product.price,
                'currency': currency,
                'quantity': quantity
            })
        
        # Generate unique reference number
        reference_number = f"ORD-{uuid.uuid4().hex[:12].upper()}"
        
        # Ensure reference number is unique
        while Order.objects.filter(reference_number=reference_number).exists():
            reference_number = f"ORD-{uuid.uuid4().hex[:12].upper()}"
        
        # Create order
        order = Order.objects.create(
            total=total,
            currency=currency,
            reference_number=reference_number,
            source=source,
            status='pending',
            shipping_address=shipping_address,
            cart=cart
        )
        
        # Create order items
        for item_data in order_items_to_create:
            OrderHasItems.objects.create(
                order=order,
                product=item_data['product'],
                price=item_data['price'],
                currency=item_data['currency'],
                quantity=item_data['quantity']
            )
        
        return order

