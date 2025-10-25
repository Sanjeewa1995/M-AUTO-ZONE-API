from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class VehiclePartRequest(models.Model):
    """
    Model for vehicle part requests
    """
    VEHICLE_TYPE_CHOICES = [
        ('car', 'Car'),
        ('truck', 'Truck'),
        ('motorcycle', 'Motorcycle'),
        ('bus', 'Bus'),
        ('van', 'Van'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Vehicle information
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    vehicle_model = models.CharField(max_length=100)
    vehicle_year = models.PositiveIntegerField()
    vehicle_image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    
    # Part information
    part_name = models.CharField(max_length=200)
    part_number = models.CharField(max_length=100, blank=True, null=True)
    part_image = models.ImageField(upload_to='part_images/', blank=True, null=True)
    part_video = models.FileField(upload_to='part_videos/', blank=True, null=True)
    
    # Request details
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle_part_requests')
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'vehicle_part_requests'
        ordering = ['-created_at']
        verbose_name = 'Vehicle Part Request'
        verbose_name_plural = 'Vehicle Part Requests'
    
    def __str__(self):
        return f"{self.vehicle_model} ({self.vehicle_year}) - {self.part_name}"
    
    @property
    def vehicle_display(self):
        return f"{self.get_vehicle_type_display()} {self.vehicle_model} ({self.vehicle_year})"
    
    def clean(self):
        super().clean()
        from datetime import datetime
        current_year = datetime.now().year
        if self.vehicle_year < 1900 or self.vehicle_year > current_year + 1:
            raise ValidationError({
                'vehicle_year': f'Vehicle year must be between 1900 and {current_year + 1}'
            })
