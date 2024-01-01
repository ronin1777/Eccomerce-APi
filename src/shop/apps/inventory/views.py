from rest_framework.viewsets import ModelViewSet
from core.global_permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import StockRecord
from .serializers import StockItemsSerializer


class StockItemsViewSet(ModelViewSet):
    serializer_class = StockItemsSerializer
    queryset = StockRecord.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
