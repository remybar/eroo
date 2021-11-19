from shortuuid import ShortUUID

from allauth.utils import get_user_model

from websites.config import MAX_WEBSITES_COUNT
from websites.models import Website

User = get_user_model()

WEBSITE_KEY_LENGTH = 16

def generate_website_key() -> str:
    """
    Generate a new website key
    """
    new_key = ShortUUID().random(length=WEBSITE_KEY_LENGTH)
    if Website.objects.filter(key=new_key).count() > 0:
        return generate_website_key()
    return new_key

def get_website(*, key: str) -> Website:
    """
    Get the website record identified by `key`
    """
    try:
        return Website.objects.get(key=key)
    except Website.DoesNotExist:
        return None

def has_reached_resource_limits(*, user: User):
    """
    Indicates if resource limits have been reached for the `user`
    """
    return Website.objects.filter(user=user).count() >= MAX_WEBSITES_COUNT
