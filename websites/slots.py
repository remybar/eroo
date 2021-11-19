from django.conf import settings

from common.services import delete_debug_data

def on_delete_website(*, airbnb_id: str, website_key: str):
    # TODO BAR: to check if it works
    if settings.USE_DEBUG_DATA_STORAGE:
        delete_debug_data(f"scrapper/{airbnb_id}/details.json")
        delete_debug_data(f"scrapper/{airbnb_id}/reviews.json")
        delete_debug_data(f"api/{website_key}/api_data.json")
        delete_debug_data(f"scrapper/{airbnb_id}")
        delete_debug_data(f"api/{website_key}")
