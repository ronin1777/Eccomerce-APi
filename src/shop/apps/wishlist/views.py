from rest_framework import viewsets
from .serializers import WishlistSerializer, WishlistItemSerializer
from .models import WishList
from ..catalog.models import Product


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return WishList.objects.filter(user=user)

    def create(self, request):
        user = self.request.user
        name = request.data['name']
        wishlist = WishList.objects.create(user=user, name=name)
        wishlist.save()
        return super().create(request)


class WishlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer

    def get_queryset(self, *args, **kwargs):
        wishlist_id = self.kwargs['wishlist_id']
        wishlist = WishList.objects.get(id=wishlist_id)
        return wishlist.get_all_items()

    def create(self,request,wishlist_id):
        wishlist = WishList.objects.get(id=wishlist_id)
        product_id = request.data['product']
        product = Product.objects.get(id=product_id)
        wishlist.add_product(product)
        return super().create(request)

    def destroy(self, request, wishlist_id, item_id):
        wishlist = WishList.objects.get(id=wishlist_id)
        wishlist.delete_item(item_id)
        return super().destroy(request, wishlist_id, item_id)





