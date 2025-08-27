from django.urls import path
from apps.organization.views import OrganizationListCreateView, OrganizationDetailView


urlpatterns = [
    path('v1/organizations/', OrganizationListCreateView.as_view(),
         name='organization-list'),
    path('v1/organizations/<int:pk>/', OrganizationDetailView.as_view(),
         name='organization-detail'),
]
