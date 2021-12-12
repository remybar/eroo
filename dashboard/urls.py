from django.urls import path, include
from django.views.generic.base import TemplateView

from dashboard.views import DashboardView, TaskView, homepage

urlpatterns = [
    path("", homepage, name="homepage"),
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('dashboard/<path:path>', DashboardView.as_view(), name="dashboard"),
    path('dashboard/task/<str:task_id>/', TaskView.as_view(), name='task'),
]
