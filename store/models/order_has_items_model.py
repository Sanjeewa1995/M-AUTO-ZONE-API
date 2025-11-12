from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class OrderHasItems(models.Model):
    """
    Model for order items - links products to orders with price snapshot
    """
    order = models.ForeignKey(
        'store.Order',
        on_delete=models.CASCADE,
        related_name='items',
        help_text="The order this item belongs to"
    )
    product = models.ForeignKey(
        'store.Product',
        on_delete=models.CASCADE,
        related_name='order_items',
        help_text="The product in this order item"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Price of the product at the time of order"
    )
    currency = models.CharField(
        max_length=3,
        default='LKR',
        help_text="Currency code (ISO 4217 format, e.g., USD, LKR)"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Quantity of the product in the order"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_has_items'
        ordering = ['-created_at']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"OrderItem {self.id} - {self.product.name} x{self.quantity} in Order {self.order.reference_number}"

