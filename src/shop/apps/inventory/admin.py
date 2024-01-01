from django.contrib import admin

from shop.apps.inventory.models import StockRecord

# Register your models here.
admin.site.register(StockRecord)
