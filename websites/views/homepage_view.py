import requests

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import FormView

from ..config import SCRAPPER_API_URL, WEBSITE_URL, MAX_WEBSITES_COUNT
from ..forms import GenerateForm
from ..models import Website
from ..utils import is_ajax, explode_airbnb_url


class HomePageView(LoginRequiredMixin, FormView):
    form_class = GenerateForm
    template_name = "websites/home.html"

    def _user_error(self, msg):
        return JsonResponse({"error_msg": msg}, status=400)

    def _internal_error(self, msg):
        return JsonResponse({"error_msg": f"Erreur interne ({msg})"}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            "MAX_WEBSITES_COUNT": MAX_WEBSITES_COUNT,
            "websites": [
                {
                    "url": WEBSITE_URL % site.key,
                    "name": site.name,
                    "generated_date": site.generated_date,
                }
                for site in Website.objects.filter(user=self.request.user)
            ],
        }
        return context

    def form_invalid(self, form):
        if not is_ajax(self.request):
            return super(HomePageView, self).form_invalid(form)
        return self._user_error("URL airbnb non fournie")

    def form_valid(self, form):
        if not is_ajax(self.request):
            return super(HomePageView, self).form_valid(form)

        rental_url = form.cleaned_data["rental_url"]

        rental_base_url, airbnb_id = explode_airbnb_url(rental_url)
        if not rental_base_url or not airbnb_id:
            return self._user_error("L'URL fournie n'est pas une URL Airbnb valide")

        # send the URL to the scrapper
        try:
            res = requests.post(
                SCRAPPER_API_URL,
                json={"provider": "airbnb", "provider_data": {"id": airbnb_id}},
            )
        except Exception:
            res = False

        if not res or res.status_code != 200:
            return self._internal_error("Impossible d'accéder à votre annonce Airbnb")

        # extract and validate the payload
        payload = res.json()
        if payload["result"] != "success" or "data" not in payload:
            return self._internal_error(
                "Impossible de récupérer les données de votre annonce Airbnb"
            )

        # generate the website and get the redirect page
        website = Website.create(self.request.user, rental_base_url, payload["data"])

        return JsonResponse({"url": WEBSITE_URL % website.key})
