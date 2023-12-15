from rest_framework import viewsets

from shop.apps.catalog.models import Category
from shop.apps.catalog.serializers.front import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.public()
    serializer_class = CategorySerializer
