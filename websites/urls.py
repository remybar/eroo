from django.urls import path
from .views import (
    WebsiteHomePage,
    WebsitePhotosPage,
    WebsiteDetailsPage,
    WebsiteContactPage,
)

urlpatterns = [
    path("<str:key>/", WebsiteHomePage.as_view(), name="website_home"),
    path("<str:key>/photos", WebsitePhotosPage.as_view(), name="website_photos"),
    path("<str:key>/details", WebsiteDetailsPage.as_view(), name="website_details"),
    path("<str:key>/contact", WebsiteContactPage.as_view(), name="website_contact"),
]
