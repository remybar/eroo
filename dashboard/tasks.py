from celery.decorators import task
from celery.utils.log import get_task_logger

from django.template import defaultfilters
from django.utils import timezone
from django.urls import reverse

from websites.models import Website
from websites.config import WEBSITE_URL
from scrapper.apis import scrap_airbnb_data

logger = get_task_logger(__name__)


@task(name="scrap_and_create_website")
def scrap_and_create_website(user_id, base_url, airbnb_id):
    """
    """
    logger.info("scrap and create website for {'airbnb_id': %s}", airbnb_id)

    try:
        data = scrap_airbnb_data(airbnb_id)
    except Exception:
        data = None

    if not data:
        return {"error": "Impossible d'accéder à votre annonce Airbnb"}

    # generate the website and get the redirect page
    try:
        website = Website.create(user_id, base_url, data)
    except Exception:
        website = None

    if not website:
        return {"error": "Impossible de créer le site web à partir des données de votre annonce"}

    return {
        "key": website.key,
        "name": website.name,
        "url": WEBSITE_URL % website.key,
        "generated_date": defaultfilters.date(timezone.localtime(website.generated_date), "d/m/Y G:i"),
        "delete_url": reverse('api_website_delete', args=[website.key]),
    }
