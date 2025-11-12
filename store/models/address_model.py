from django.db import models


class Address(models.Model):
    """
    Model for shipping/billing addresses
    """
    first_name = models.CharField(
        max_length=100,
        help_text="First name of the recipient"
    )
    last_name = models.CharField(
        max_length=100,
        help_text="Last name of the recipient"
    )
    country = models.CharField(
        max_length=100,
        help_text="Country name"
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="State or province"
    )
    post_code = models.CharField(
        max_length=20,
        help_text="Postal or ZIP code"
    )
    city = models.CharField(
        max_length=100,
        help_text="City name"
    )
    address1 = models.CharField(
        max_length=255,
        help_text="Street address line 1"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'addresses'
        ordering = ['-created_at']
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        indexes = [
            models.Index(fields=['country']),
            models.Index(fields=['city']),
            models.Index(fields=['post_code']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.address1}, {self.city}, {self.country}"

