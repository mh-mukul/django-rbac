from django.urls import path

from apps.user.views import UserListCreateView, UserDetailView

# # Define the urlpatterns
urlpatterns = [
    path('v1/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('v1/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
