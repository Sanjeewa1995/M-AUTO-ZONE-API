import uuid
from django.db import models


class Cart(models.Model):
    """
    Model for shopping cart with session-based identification
    """
    session_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Unique session identifier for the cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        ordering = ['-created_at']
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"Cart {self.session_id}"

