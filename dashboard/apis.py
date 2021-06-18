import requests

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template import defaultfilters
from django.utils import timezone
from django.urls import reverse

from websites.utils import is_ajax, explode_airbnb_url
from websites.config import SCRAPPER_API_URL, WEBSITE_URL, MAX_WEBSITES_COUNT
from websites.models import Website


def _user_error(msg):
    return HttpResponse(reason=msg, status=400)


def _internal_error(msg):
    return HttpResponse(reason=msg, status=500)


@login_required
def api_website_create(request):
    if not is_ajax(request) or "rental_url" not in request.POST:
        return _internal_error("mauvaise requête")

    if not request.POST["rental_url"]:
        return _internal_error("URL de l'annonce non fournie")

    rental_base_url, airbnb_id = explode_airbnb_url(request.POST["rental_url"])
    if not rental_base_url or not airbnb_id:
        return _user_error("L'URL fournie n'est pas une URL Airbnb valide")

    # check if the current user does not exceed limitations
    if Website.objects.filter(user=request.user).count() >= MAX_WEBSITES_COUNT:
        return _user_error("Limite de nombre de sites atteinte. Supprimez-en un pour pouvoir en créer un nouveau.")

    # send the URL to the scrapper
    try:
        res = requests.post(
            SCRAPPER_API_URL,
            json={"provider": "airbnb", "provider_data": {"id": airbnb_id}},
        )
    except Exception:
        res = False

    if not res or res.status_code != 200:
        return _internal_error("Impossible d'accéder à votre annonce Airbnb")

    # extract and validate the payload
    payload = res.json()
    if payload["result"] != "success" or "data" not in payload:
        return _internal_error(
            "Impossible de récupérer les données de votre annonce Airbnb"
        )

    # generate the website and get the redirect page
    website = Website.create(request.user, rental_base_url, payload["data"])

    return JsonResponse({
        "key": website.key,
        "name": website.name,
        "url": WEBSITE_URL % website.key,
        "generated_date": defaultfilters.date(timezone.localtime(website.generated_date), "d/m/Y G:i"),
        "delete_url": reverse('api_website_delete', args=[website.key]),
    })


@login_required
def api_website_delete(request, key):
    if not is_ajax(request):
        return _internal_error("mauvaise requête")

    try:
        website = Website.objects.get(key=key)
    except Website.DoesNotExist:
        return _user_error("Ce site n'existe pas")

    website.delete()
    return JsonResponse({"key": key})
