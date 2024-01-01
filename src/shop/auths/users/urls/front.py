from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from shop.auths.users.views.front import RegisterView, LoginAPIView, LogoutAPIView, CreateProfileView, \
    RetrieveUpdateProfileView

app_name = 'users-front'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('logout/', LogoutAPIView.as_view(), name="user_logout"),
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"),
    path('update_profile/<int:user_id>/', RetrieveUpdateProfileView.as_view(), name="update_Retrieve_profile"),

]

