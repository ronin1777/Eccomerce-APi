from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shop.apps.order.views import OrderViewSet, OrderItemViewSet

app_name = "orders"

router = DefaultRouter()
router.register(r"^(?P<order_id>\d+)/order-items", OrderItemViewSet)
router.register(r"", OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
]