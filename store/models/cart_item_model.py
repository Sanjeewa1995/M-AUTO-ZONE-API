from django.db import models
from django.core.validators import MinValueValidator


class CartItem(models.Model):
    """
    Model for cart items - links products to carts
    """
    cart = models.ForeignKey(
        'store.Cart',
        on_delete=models.CASCADE,
        related_name='items',
        help_text="The cart this item belongs to"
    )
    product = models.ForeignKey(
        'store.Product',
        on_delete=models.CASCADE,
        related_name='cart_items',
        help_text="The product in this cart item"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Quantity of the product in the cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_items'
        ordering = ['-created_at']
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = [['cart', 'product']]  # Prevent duplicate products in same cart

    def __str__(self):
        return f"CartItem {self.id} - {self.product.name} in Cart {self.cart.session_id}"

