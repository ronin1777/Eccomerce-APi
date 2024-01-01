from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import StockRecord
from .utils import check_quantity_and_set_status


@receiver(post_save, sender=StockRecord)
def update_product_availability_status_post_save(sender, instance, created, **kwargs):
    if created:
        check_quantity_and_set_status(instance)


@receiver(pre_save, sender=StockRecord)
def update_product_availability_status_pre_save(sender, instance, **kwargs):
    if instance.pk:  # Check if instance is being updated
        old_instance = StockRecord.objects.get(pk=instance.pk)
        if old_instance.num_stock != instance.num_stock:
            # Update product status based on quantity in stock
            check_quantity_and_set_status(instance)