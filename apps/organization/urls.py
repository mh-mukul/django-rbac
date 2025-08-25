from django.urls import path
from apps.organization.views import OrganizationListView, OrganizationDetailView, OrganizationCreateView


urlpatterns = [
    path('v1/organizations/', OrganizationListView.as_view(),
         name='organization-list'),
    path('v1/organizations/<int:pk>/', OrganizationDetailView.as_view(),
         name='organization-detail'),
    path('v1/organizations/create/', OrganizationCreateView.as_view(),
         name='organization-create'),
]
