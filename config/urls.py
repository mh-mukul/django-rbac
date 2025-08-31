"""
URL configuration for django-rbac project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.conf import settings
from django.http import JsonResponse
from django.urls import path, include


def healthcheck(request):
    return JsonResponse({"status": "ok"})


# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', healthcheck),
    path('api/', include('apps.authentication.urls')),
    path('api/', include('apps.organization.urls')),
    path('api/', include('apps.user.urls')),
    path('api/', include('apps.authorization.urls')),
]

# # Include debug toolbar URLs in development
# if settings.DEBUG:
#     try:
#         import debug_toolbar
#         urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
#     except ImportError:
#         pass
