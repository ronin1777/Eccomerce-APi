from rest_framework import serializers

from shop.apps.wishlist.models import WishList, WishlistItem


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        return WishlistSerializer(obj.get_all_items(), many=True).data

    class Meta:
        model = WishList
        fields = ['id', 'name', 'user', 'items']


class WishlistItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    variation = serializers.JSONField(read_only=True)
    variation_hash = serializers.CharField(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'product', 'variation', 'variation_hash']
