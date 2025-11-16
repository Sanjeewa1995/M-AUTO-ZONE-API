from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def update_request_status_on_product_creation(sender, instance, created, **kwargs):
    """
    Update the vehicle part request status to 'completed' when a product is added
    """
    if created and instance.request:
        # Only update if the request is not already completed or cancelled
        if instance.request.status in ['pending', 'in_progress']:
            instance.request.status = 'completed'
            instance.request.save(update_fields=['status'])

