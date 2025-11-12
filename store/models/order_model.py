from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Order(models.Model):
    """
    Model for customer orders
    """
    SOURCE_CHOICES = [
        ('web', 'Web'),
        ('android', 'Android'),
        ('ios', 'iOS'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Total amount of the order"
    )
    currency = models.CharField(
        max_length=3,
        default='LKR',
        help_text="Currency code (ISO 4217 format, e.g., USD, LKR)"
    )
    reference_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique reference number for the order"
    )
    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES,
        help_text="Platform where the order was placed"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the order"
    )
    shipping_address = models.ForeignKey(
        'store.Address',
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="Shipping address for this order"
    )
    cart = models.ForeignKey(
        'store.Cart',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='orders',
        help_text="The cart this order was created from (if applicable)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(fields=['reference_number']),
            models.Index(fields=['status']),
            models.Index(fields=['source']),
        ]

    def __str__(self):
        return f"Order {self.reference_number} - {self.total} {self.currency}"

