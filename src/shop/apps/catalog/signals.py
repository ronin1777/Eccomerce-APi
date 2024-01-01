from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shop.apps.catalog.models import Product, AvailabilityStatuses


@receiver(post_save, sender=Product)
def update_product_availability_status(sender, instance, created, **kwargs):
    if instance.pk:
        if Product.availability_status == AvailabilityStatuses.low_in_stock:
            #Todo send mail to notif that stock of product is low