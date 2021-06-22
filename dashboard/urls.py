from django.urls import path
from .views import DashboardView, homepage
from .apis import api_website_create, api_website_delete

urlpatterns = [
    path("", homepage, name="homepage"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),

    # API
    path("api/v1/website/create", api_website_create, name="api_website_create"),
    path("api/v1/website/delete/<str:key>", api_website_delete, name="api_website_delete"),
]
