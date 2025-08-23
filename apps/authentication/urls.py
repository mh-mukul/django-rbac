from django.urls import path
from apps.authentication.views import (
    UserLoginView,
    RefreshTokenView,
    UserLogoutView,
)


urlpatterns = [
    path('v1/login/', UserLoginView.as_view(), name='user-login'),
    path('v1/refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('v1/logout/', UserLogoutView.as_view(), name='user-logout'),
]
