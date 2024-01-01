from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', CartAPIView.as_view(), name='basket_detail'),
    path('add/<int:product_id>/', AddToBasketAPIView.as_view()),
    path('add_quantity/<int:product_id>/',
         BasketItemAddQuantityAPIView.as_view(),
         name='item_add_quantity'),
    path('minus_quantity/<int:product_id>/',
         BasketItemMinusQuantityAPIView.as_view(),
         name='item_minus_quantity'),
    path('clear/', BasketClearAPIView.as_view(), name='basket_clear')
]