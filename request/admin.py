from django.contrib import admin
from .models import VehiclePartRequest


@admin.register(VehiclePartRequest)
class VehiclePartRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for VehiclePartRequest model
    """
    list_display = [
        'id', 'user', 'vehicle_display', 'part_name', 
        'status', 'created_at'
    ]
    list_filter = [
        'vehicle_type', 'status', 'vehicle_year', 'created_at'
    ]
    search_fields = [
        'vehicle_model', 'part_name', 'part_number', 
        'user__email', 'user__first_name', 'user__last_name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Vehicle Information', {
            'fields': ('vehicle_type', 'vehicle_model', 'vehicle_year', 'vehicle_image')
        }),
        ('Part Information', {
            'fields': ('part_name', 'part_number', 'part_image', 'part_video')
        }),
        ('Request Details', {
            'fields': ('user', 'description', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def vehicle_display(self, obj):
        return obj.vehicle_display
    vehicle_display.short_description = 'Vehicle'
