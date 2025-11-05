from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Product(models.Model):
    """
    Model for products related to vehicle part requests
    """
    request = models.ForeignKey(
        'request.VehiclePartRequest',
        on_delete=models.CASCADE,
        related_name='products',
        help_text="The vehicle part request this product relates to"
    )
    name = models.CharField(
        max_length=200,
        help_text="Name of the product"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the product"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Price of the product"
    )
    image = models.ImageField(
        upload_to='product_images/',
        blank=True,
        null=True,
        help_text="Image of the product"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} - {self.request}"
