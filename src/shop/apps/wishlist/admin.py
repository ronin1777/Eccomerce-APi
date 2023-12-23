from django.contrib import admin

from shop.apps.wishlist.models import WishList, WishlistItem


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    list_display = ['user', 'product']

    def get_product_title(self, obj):
        return obj.product.title if obj.product else None

    get_product_title.short_description = 'Product Title'


@admin.register(WishList)
class WishlistAdmin(admin.ModelAdmin):
    inlines = [WishlistItemInline]

    list_display = ['user', 'name']
