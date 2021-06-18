from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from websites.config import MAX_WEBSITES_COUNT, WEBSITE_URL
from websites.models import Website


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
