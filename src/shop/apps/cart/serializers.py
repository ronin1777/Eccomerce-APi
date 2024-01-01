from rest_framework import serializers

from .models import CartModel, CartItems
from ..catalog.serializers.admin import ProductSerializers
from ...auths.users.serializers.front import ProfileSerializer


class CartSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()

    class Meta:
        model = CartModel
        fields = ('user', 'owner_username', 'product', 'quantity', 'total_price')

    def get_owner_username(self, obj):
        user = obj.user
        user_serializer = ProfileSerializer(instance=user)
        return user_serializer.data['username']


class CartItemsSerializer(serializers.ModelSerializer):
    product_title = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = ('product', 'product_name', 'quantity', 'total_price')

    def get_product_title(self, obj):
        product = obj.product
        serializer_product = ProductSerializers(instance=product)
        return serializer_product.data['title']


class SessionBasketSerializer(serializers.Serializer):

    def to_representation(self, instance):
        items = []
        for item in instance:
            item_data = item.copy()
            item_data['product_title'] = item_data.get('product').title
            item_data['product'] = item_data.pop('product').id
            items.append(item_data)
        return {'items': items}























