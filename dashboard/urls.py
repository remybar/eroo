from django.urls import path
from .views import DashboardView
from .apis import api_website_create, api_website_delete

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),

    # API
    path("api/v1/website/create", api_website_create, name="api_website_create"),
    path("api/v1/website/delete/<str:key>", api_website_delete, name="api_website_delete"),

]
