from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from shop.apps.rates.models import Rating
from shop.apps.rates.serializers import RatingSerializer


class RatingListCreate(ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
