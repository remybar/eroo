import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template import defaultfilters
from django.utils import timezone
from django.urls import reverse

from websites.utils import is_ajax, explode_airbnb_url
from websites.config import WEBSITE_URL, MAX_WEBSITES_COUNT
from websites.models import Website

from scrapper.views import scrap_airbnb_data


_logger = logging.getLogger('websites')


def _user_error(msg):
    return JsonResponse({"error": msg}, status=400)


def _internal_error(msg):
    return JsonResponse({"error": msg}, status=500)


@login_required
def api_website_create(request):
    if not is_ajax(request) or "rental_url" not in request.POST:
        return _internal_error("mauvaise requête")

    if not request.POST["rental_url"]:
        return _internal_error("URL de l'annonce non fournie")

    _logger.info("website create {'url': %s}", request.POST["rental_url"])

    rental_base_url, airbnb_id = explode_airbnb_url(request.POST["rental_url"])
    if not rental_base_url or not airbnb_id:
        return _user_error("L'URL fournie n'est pas une URL Airbnb valide")

    # check if the current user does not exceed limitations
    if Website.objects.filter(user=request.user).count() >= MAX_WEBSITES_COUNT:
        return _user_error("Limite de nombre de sites atteinte. Supprimez-en un pour pouvoir en créer un nouveau.")

    # send the URL to the scrapper
    try:
        data = scrap_airbnb_data(airbnb_id)
    except Exception:
        return _internal_error("Impossible d'accéder à votre annonce Airbnb")

    # generate the website and get the redirect page
    website = Website.create(request.user, rental_base_url, data)

    return JsonResponse({
        "key": website.key,
        "name": website.name,
        "url": WEBSITE_URL % website.key,
        "generated_date": defaultfilters.date(timezone.localtime(website.generated_date), "d/m/Y G:i"),
        "delete_url": reverse('api_website_delete', args=[website.key]),
    })


@login_required
def api_website_delete(request, key):
    _logger.info("delete website {'id': %s}", key)

    if not is_ajax(request):
        return _internal_error("mauvaise requête")

    try:
        website = Website.objects.get(key=key)
    except Website.DoesNotExist:
        return _user_error("Ce site n'existe pas")

    website.delete()
    return JsonResponse({"key": key})
