from celery import shared_task

from websites.services import generate_website_from_airbnb
from bookings.models import Housing

@shared_task
def task_generate_website_from_airbnb(*, user_id: int, housing: Housing):
    generate_website_from_airbnb(user_id=user_id, housing=housing)
