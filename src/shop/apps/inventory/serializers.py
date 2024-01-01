from shop.apps.inventory.models import StockRecord
from rest_framework import serializers
from django.urls import reverse


class StockItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)
    product_price = serializers.CharField(source='product.price',
                                          read_only=True)
    class Meta:
        model = StockRecord
        fields = ['id', 'product', 'product_name',
                  'buy_price', 'sku', 'quantity_in_stock',
                  'quantity_sold', 'threshold_low_stack', 'product_price']

    def get_product_name(self, obj):
        return obj.product.title

    def get_product_link(self, obj):
        return reverse('products-detail', kwargs={'pk': obj.product.pk})

