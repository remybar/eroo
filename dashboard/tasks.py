from celery import shared_task
from celery.utils.log import get_task_logger

from django.template import defaultfilters
from django.utils import timezone
from django.urls import reverse

from websites.models import Website
from websites.config import WEBSITE_URL
from scrapper.apis import scrap_and_convert

logger = get_task_logger(__name__)


@shared_task
def scrap_and_create_website(user_id, base_url, airbnb_id):
    """
    """
    logger.info("scrap and create website for {'airbnb_id': %s}", airbnb_id)

    try:
        data = scrap_and_convert(airbnb_id)
    except Exception:
        data = None

    if not data:
        return {
            "result": "error",
            "msg": "Impossible d'accéder à votre annonce Airbnb"
        }

    # generate the website and get the redirect page
    try:
        website = Website.create(user_id, base_url, data)
    except Exception as e:
        logger.exception(str(e))
        website = None

    if not website:
        return {
            "result": "error",
            "msg": "Impossible de créer le site web à partir des données de votre annonce"
        }

    return {
        "result": "success",
        "key": website.key,
        "name": website.name,
        "url": WEBSITE_URL % website.key,
        "generated_date": defaultfilters.date(timezone.localtime(website.generated_date), "d/m/Y G:i"),
        "delete_url": reverse('api_website_delete', args=[website.key]),
    }
