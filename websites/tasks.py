from celery import shared_task

from allauth.utils import get_user_model

from websites.services import generate_website_from_airbnb
from bookings.models import Housing

User = get_user_model()

@shared_task
def task_generate_website_from_airbnb(*, user_id: int, housing_id: int):
    generate_website_from_airbnb(
        user=User.objects.get(pk=user_id),
        housing=Housing.objects.get(pk=housing_id),
    )
