from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse

from celery import current_app
from websites.config import MAX_WEBSITES_COUNT, WEBSITE_URL
from websites.models import Website

# TODO RBA: move to a common module to handle CRUD apis in a same way in the whole project.
# TODO RBA: try to improve it.
def ident(url):
    return url

def strip_id(url):
    return url.removesuffix('0/')

CRUD_ENDPOINTS = (
    ('list', None, ident),
    ('detail', [0], strip_id),
    ('create', None, ident),
    ('update', [0], strip_id),
    ('delete', [0], strip_id),
)

def homepage(request):
    if request.user.is_authenticated:
        redirect("dashboard")
    return redirect("account_signup")

def crud_urls(namespace, exclude_endpoints=None):
    endpoints = (
        (name, args, func)
        for name, args, func in CRUD_ENDPOINTS
        if name not in exclude_endpoints
    ) if exclude_endpoints else CRUD_ENDPOINTS

    return {
        name: func(reverse(f'{namespace}:{name}', args=args))
        for name, args, func in endpoints
    }

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'config': {
                'username': self.request.user.username,
                'urls': {
                    'seasons': crud_urls('bookings:seasons'),
                    'housings': crud_urls('bookings:housings'),
                },
            },
        }
        # context |= {
        #     "MAX_WEBSITES_COUNT": MAX_WEBSITES_COUNT,
        #     "websites": [
        #         {
        #             "key": site.key,
        #             "url": WEBSITE_URL % site.key,
        #             "name": site.name,
        #             "generated_date": site.generated_date,
        #         }
        #         for site in Website.objects.filter(user=self.request.user)
        #     ],
        # }
        return context


class TaskView(View):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['data'] = task.get()

        return JsonResponse(response_data)
