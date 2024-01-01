from django.urls import path
from .views import RatingListCreate

app_name = 'rating'

urlpatterns = [
    path('ratings/', RatingListCreate.as_view(), name='rating-list-create'),
]
