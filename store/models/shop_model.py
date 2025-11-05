from django.db import models
from django.core.validators import RegexValidator


class Shop(models.Model):
    """
    Model for shops
    """
    name = models.CharField(
        max_length=200,
        help_text="Name of the shop"
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )],
        help_text="Contact phone number"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Contact email address"
    )
    active = models.BooleanField(
        default=True,
        help_text="Whether the shop is currently active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'shops'
        ordering = ['-created_at']
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'
    
    def __str__(self):
        return self.name


class RequestHasShop(models.Model):
    """
    Model linking vehicle part requests to shops
    """
    request = models.ForeignKey(
        'request.VehiclePartRequest',
        on_delete=models.CASCADE,
        related_name='request_shops',
        help_text="The vehicle part request"
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='shop_requests',
        help_text="The shop associated with this request"
    )
    message = models.TextField(
        blank=True,
        null=True,
        help_text="Optional message related to this request-shop association"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'request_has_shops'
        ordering = ['-created_at']
        verbose_name = 'Request Has Shop'
        verbose_name_plural = 'Request Has Shops'
        unique_together = [['request', 'shop']]
    
    def __str__(self):
        return f"{self.request} - {self.shop}"


