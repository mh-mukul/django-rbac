"""
URL configuration for django-rbac project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

# API URL patterns
api_urlpatterns = [
    path('users/', include('apps.users.urls')),
]

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    path('api/', include('apps.authentication.urls')),
]

# # Include debug toolbar URLs in development
# if settings.DEBUG:
#     try:
#         import debug_toolbar
#         urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
#     except ImportError:
#         pass
