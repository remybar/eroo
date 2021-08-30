from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from celery import current_app
from websites.config import MAX_WEBSITES_COUNT, WEBSITE_URL
from websites.models import Website


def homepage(request):
    if request.user.is_authenticated:
        redirect("dashboard")
    return redirect("account_signup")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            "MAX_WEBSITES_COUNT": MAX_WEBSITES_COUNT,
            "websites": [
                {
                    "key": site.key,
                    "url": WEBSITE_URL % site.key,
                    "name": site.name,
                    "generated_date": site.generated_date,
                }
                for site in Website.objects.filter(user=self.request.user)
            ],
        }
        return context


class TaskView(View):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['data'] = task.get()

        return JsonResponse(response_data)
