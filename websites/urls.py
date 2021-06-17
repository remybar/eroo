from django.urls import path
from .views import (
    HomePageView,
    WebsiteHomePage,
    WebsitePhotosPage,
    WebsiteDetailsPage,
    WebsiteContactPage,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("websites/<str:key>/", WebsiteHomePage.as_view(), name="website_home"),
    path("websites/<str:key>/photos", WebsitePhotosPage.as_view(), name="website_photos"),
    path("websites/<str:key>/details", WebsiteDetailsPage.as_view(), name="website_details"),
    path("websites/<str:key>/contact", WebsiteContactPage.as_view(), name="website_contact"),
]
