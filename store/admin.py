from django.contrib import admin
from .models import Shop, RequestHasShop, Product


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
