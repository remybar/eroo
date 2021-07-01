import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from websites.utils import is_ajax, explode_airbnb_url
from websites.config import MAX_WEBSITES_COUNT
from websites.models import Website

from .tasks import scrap_and_create_website


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
    if Website.has_reached_resource_limits(request.user):
        return _user_error("Limite de nombre de sites atteinte. Supprimez-en un pour pouvoir en créer un nouveau.")

    # scrap and create the website in background.
    # the task id is provided to allow the client to poll task result
    task = scrap_and_create_website.delay(request.user, rental_base_url, airbnb_id)

    return JsonResponse({"task_id": task.id}, status=202)


@login_required
def api_website_delete(request, key):
    _logger.info("delete website {'id': %s}", key)

    if not is_ajax(request):
        return _internal_error("mauvaise requête")

    website = Website.get_website(key)

    if website:
        website.delete()
        return JsonResponse({"key": key})
    else:
        return _user_error("Ce site n'existe pas")
