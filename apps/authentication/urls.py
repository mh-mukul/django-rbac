from django.urls import path
from apps.authentication.views import (
    LoginView,
    RefreshTokenView,
    LogoutView,
)


urlpatterns = [
    path('v1/login/', LoginView.as_view(), name='login'),
    path('v1/refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('v1/logout/', LogoutView.as_view(), name='logout'),
]
