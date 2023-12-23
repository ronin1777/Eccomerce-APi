from django.urls import path
from rest_framework.routers import SimpleRouter

from shop.auths.users.views.admin import AdminLoginView

app_name = 'users-admin'

router = SimpleRouter()
urlpatterns = [
                  path('login/', AdminLoginView.as_view(), )
              ] + router.urls
