from django.urls import path
from apps.authorization.views import (
    ModuleListCreateView,
    ModuleDetailsView,
    PermissionListCreateView,
    PermissionDetailsView,
    RoleListCreateView,
    RoleDetailsView,
)

urlpatterns = [
    path('v1/modules/', ModuleListCreateView.as_view(), name='module-list'),
    path('v1/modules/<int:pk>/', ModuleDetailsView.as_view(), name='module-detail'),
    path('v1/permissions/', PermissionListCreateView.as_view(),
         name='permission-list'),
    path('v1/permissions/<int:pk>/', PermissionDetailsView.as_view(),
         name='permission-detail'),
    path('v1/roles/', RoleListCreateView.as_view(), name='role-list'),
    path('v1/roles/<int:pk>/', RoleDetailsView.as_view(), name='role-detail'),
]
