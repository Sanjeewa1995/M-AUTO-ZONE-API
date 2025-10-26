from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from .compression_utils import (
    compress_vehicle_image, 
    compress_part_image, 
    compress_part_video,
    FileSizeValidator
)

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
        ('suv', 'SUV'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    vehicle_type = models.CharField(
        max_length=20, 
        choices=VEHICLE_TYPE_CHOICES,
        help_text="Type of vehicle"
    )
    vehicle_model = models.CharField(
        max_length=100,
        help_text="Model of the vehicle (e.g., Toyota Camry, Honda Civic)"
    )
    vehicle_year = models.PositiveIntegerField(
        help_text="Year of the vehicle"
    )
    
    # Part Information
    part_name = models.CharField(
        max_length=200,
        help_text="Name of the part being requested"
    )
    part_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Part number if available"
    )
    
    # Media Files
    vehicle_image = models.ImageField(
        upload_to='vehicle_images/',
        blank=True,
        null=True,
        help_text="Image of the vehicle"
    )
    part_image = models.ImageField(
        upload_to='part_images/',
        blank=True,
        null=True,
        help_text="Image of the part"
    )
    part_video = models.FileField(
        upload_to='part_videos/',
        blank=True,
        null=True,
        help_text="Video of the part"
    )
    
    # Request Details
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicle_part_requests',
        help_text="User who made the request"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Additional description or notes"
    )
    
    # Status and Timestamps
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the request"
    )
    
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
        """Return formatted vehicle information"""
        return f"{self.get_vehicle_type_display()} {self.vehicle_model} ({self.vehicle_year})"
    
    def clean(self):
        """Validate model fields"""
        super().clean()
        
        # Validate vehicle year
        from datetime import datetime
        current_year = datetime.now().year
        if self.vehicle_year < 1900 or self.vehicle_year > current_year + 1:
            raise ValidationError({
                'vehicle_year': f'Vehicle year must be between 1900 and {current_year + 1}'
            })
    
    def save(self, *args, **kwargs):
        """Override save to compress media files"""
        # Compress images before saving
        if self.vehicle_image and hasattr(self.vehicle_image, 'file'):
            if isinstance(self.vehicle_image.file, UploadedFile):
                # Validate file
                is_valid, error_msg = FileSizeValidator.validate_image_file(self.vehicle_image.file)
                if not is_valid:
                    raise ValidationError({'vehicle_image': error_msg})
                
                # Compress file
                compressed_file = compress_vehicle_image(self.vehicle_image.file)
                self.vehicle_image = compressed_file
        
        if self.part_image and hasattr(self.part_image, 'file'):
            if isinstance(self.part_image.file, UploadedFile):
                # Validate file
                is_valid, error_msg = FileSizeValidator.validate_image_file(self.part_image.file)
                if not is_valid:
                    raise ValidationError({'part_image': error_msg})
                
                # Compress file
                compressed_file = compress_part_image(self.part_image.file)
                self.part_image = compressed_file
        
        if self.part_video and hasattr(self.part_video, 'file'):
            if isinstance(self.part_video.file, UploadedFile):
                # Validate file
                is_valid, error_msg = FileSizeValidator.validate_video_file(self.part_video.file)
                if not is_valid:
                    raise ValidationError({'part_video': error_msg})
                
                # Compress file (placeholder for now)
                compressed_file = compress_part_video(self.part_video.file)
                self.part_video = compressed_file
        
        super().save(*args, **kwargs)
