from django.contrib import admin
from .models import Shop, RequestHasShop, Product, Order, OrderHasItems, Address


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """
    Admin configuration for Shop model
    """
    list_display = [
        'id', 'name', 'phone_number', 'email', 'active', 'created_at'
    ]
    list_filter = [
        'active', 'created_at', 'updated_at'
    ]
    search_fields = [
        'name', 'phone_number', 'email'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Shop Information', {
            'fields': ('name', 'phone_number', 'email', 'active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RequestHasShop)
class RequestHasShopAdmin(admin.ModelAdmin):
    """
    Admin configuration for RequestHasShop model
    """
    list_display = [
        'id', 'request', 'shop', 'created_at'
    ]
    list_filter = [
        'created_at', 'updated_at'
    ]
    search_fields = [
        'request__part_name', 'request__vehicle_model', 'shop__name', 'message'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Association Information', {
            'fields': ('request', 'shop', 'message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model
    """
    list_display = [
        'id', 'name', 'request', 'price', 'created_at'
    ]
    list_filter = [
        'created_at', 'updated_at'
    ]
    search_fields = [
        'name', 'description', 'request__part_name', 'request__vehicle_model'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('request', 'name', 'description', 'price', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class OrderHasItemsInline(admin.TabularInline):
    """
    Inline admin for OrderHasItems to display order items within Order admin
    """
    model = OrderHasItems
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = ['product', 'price', 'currency', 'quantity', 'created_at', 'updated_at']
    can_delete = False
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model
    """
    list_display = [
        'id', 'reference_number', 'user_display', 'total', 'currency', 
        'status', 'source', 'item_count', 'created_at'
    ]
    list_filter = [
        'status', 'source', 'currency', 'created_at', 'updated_at'
    ]
    search_fields = [
        'reference_number', 'user__email', 'user__first_name', 
        'user__last_name', 'shipping_address__first_name',
        'shipping_address__last_name', 'shipping_address__city',
        'shipping_address__country'
    ]
    readonly_fields = [
        'reference_number', 'created_at', 'updated_at', 
        'total_display', 'item_count_display'
    ]
    ordering = ['-created_at']
    inlines = [OrderHasItemsInline]
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related and prefetch_related
        """
        qs = super().get_queryset(request)
        return qs.select_related('user', 'shipping_address', 'cart').prefetch_related('items')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('reference_number', 'user', 'status', 'source', 'total', 'currency')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address',)
        }),
        ('Cart Information', {
            'fields': ('cart',),
            'classes': ('collapse',)
        }),
        ('Order Summary', {
            'fields': ('total_display', 'item_count_display'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_display(self, obj):
        """
        Display user information with fallback for None
        """
        if obj.user:
            return f"{obj.user.email} ({obj.user.get_full_name()})"
        return "No user"
    user_display.short_description = 'User'
    user_display.admin_order_field = 'user__email'
    
    def item_count(self, obj):
        """
        Display the number of items in the order
        """
        # Use prefetched items if available to avoid extra queries
        if hasattr(obj, '_prefetched_objects_cache') and 'items' in obj._prefetched_objects_cache:
            return len(obj._prefetched_objects_cache['items'])
        return obj.items.count()
    item_count.short_description = 'Items'
    
    def item_count_display(self, obj):
        """
        Display item count in detail view
        """
        # Use prefetched items if available to avoid extra queries
        if hasattr(obj, '_prefetched_objects_cache') and 'items' in obj._prefetched_objects_cache:
            count = len(obj._prefetched_objects_cache['items'])
        else:
            count = obj.items.count()
        return f"{count} item(s)"
    item_count_display.short_description = 'Total Items'
    
    def total_display(self, obj):
        """
        Display formatted total with currency
        """
        return f"{obj.total} {obj.currency}"
    total_display.short_description = 'Order Total'


@admin.register(OrderHasItems)
class OrderHasItemsAdmin(admin.ModelAdmin):
    """
    Admin configuration for OrderHasItems model (standalone view)
    """
    list_display = [
        'id', 'order', 'product', 'price', 'currency', 
        'quantity', 'subtotal', 'created_at'
    ]
    list_filter = [
        'currency', 'created_at', 'updated_at'
    ]
    search_fields = [
        'order__reference_number', 'product__name', 
        'product__description'
    ]
    readonly_fields = ['created_at', 'updated_at', 'subtotal_display']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Order Item Information', {
            'fields': ('order', 'product', 'price', 'currency', 'quantity')
        }),
        ('Calculations', {
            'fields': ('subtotal_display',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subtotal(self, obj):
        """
        Calculate and display subtotal for list view
        """
        from decimal import Decimal
        return Decimal(str(obj.price)) * obj.quantity
    subtotal.short_description = 'Subtotal'
    
    def subtotal_display(self, obj):
        """
        Display formatted subtotal in detail view
        """
        from decimal import Decimal
        subtotal = Decimal(str(obj.price)) * obj.quantity
        return f"{subtotal} {obj.currency}"
    subtotal_display.short_description = 'Subtotal'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Admin configuration for Address model
    """
    list_display = [
        'id', 'first_name', 'last_name', 'city', 
        'country', 'post_code', 'created_at'
    ]
    list_filter = [
        'country', 'city', 'created_at', 'updated_at'
    ]
    search_fields = [
        'first_name', 'last_name', 'address1', 
        'city', 'country', 'post_code', 'state'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Recipient Information', {
            'fields': ('first_name', 'last_name')
        }),
        ('Address Details', {
            'fields': ('address1', 'city', 'state', 'post_code', 'country')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
