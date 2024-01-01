from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from shop.apps.order.models import OrderItem, Order

from shop.apps.order.serializers import OrderItemSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD order items that are associated with the current order id.
    """

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        res = super().get_queryset()
        order_id = self.kwargs.get("order_id")
        return res.filter(order__id=order_id)

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get("order_id"))
        serializer.save(order=order)


