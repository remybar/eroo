"""
Eroo URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("yaap/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path("accounts/", include("allauth.urls")),
    path("websites/", include("websites.urls")),
    path("", include("dashboard.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
