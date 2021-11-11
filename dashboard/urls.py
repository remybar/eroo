from django.urls import path, include
from django.views.generic.base import TemplateView

from dashboard.views import DashboardView, TaskView, homepage
from dashboard.apis.website import (
    api_website_create, api_website_delete
)

urlpatterns = [
    path("", homepage, name="homepage"),
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('dashboard/<path:path>', DashboardView.as_view(), name="dashboard"),
    path('dashboard/task/<str:task_id>/', TaskView.as_view(), name='task'),

    # API
    path("api/v1/website/create", api_website_create, name="api_website_create"),
    path("api/v1/website/delete/<str:key>", api_website_delete, name="api_website_delete"),
]
