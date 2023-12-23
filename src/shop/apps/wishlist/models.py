from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from shop.apps.catalog.models import Product


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_wishlist')
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'shop_wishlist'
        verbose_name = _('Wishlist')
        verbose_name_plural = _('Wishlists')

    def __str__(self):
        return f"wish list {self.name} for {self.user}"

    def add_product(self, product):

        items = WishlistItem.objects.filter(wishlist=self, product=product)

        item = WishlistItem.objects.create(wishlist=self, product=product)
        item.save()
        self.save()

    def get_all_items(self):

        return WishlistItem.objects.filter(wishlist=self)

    def find_item(self, product, variation=None):

        return WishlistItem.objects.filter(wishlist=self, product=product)

    def delete_item(self, item_id):

        WishlistItem.objects.get(pk=item_id).delete()
        self.save()


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_product')

    def save(self, **kwargs):
        existing_items = WishlistItem.objects.filter(wishlist=self.wishlist, product=self.product,)

        if existing_items.exists() and self.pk is None:
            # Product already exists in wishlist, so raise an error
            raise ValidationError(_("This product is already in your wishlist."))

        super().save(**kwargs)
