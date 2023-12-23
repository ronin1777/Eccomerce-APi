# from shop.apps.wishlist.views import WishlistViewSet, WishlistItemViewSet
# from django.urls import path
#
#

# urlpatterns = [
#     path('wishlists/<int:pk>/', WishlistViewSet.as_view(), name='wishlist-detail'),
#     path('wishlists/<int:wishlist_id>/items/<int:pk>/', WishlistItemViewSet.as_view(), name='wishlistItem-detail'),
# ]
from rest_framework.routers import SimpleRouter

from shop.apps.wishlist.views import WishlistViewSet, WishlistItemViewSet
app_name = 'wishlist'
router = SimpleRouter()
router.register('wishlist', WishlistViewSet, basename='WishList')
router.register('wishListItems', WishlistItemViewSet, basename='WishListItems')
urlpatterns = [] + router.urls
