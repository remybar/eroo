import airbnb
import logging
import re

from django.conf import settings

from websites.utils import save_debug_data

REVIEWS_COUNT = 5

_logger = logging.getLogger('scrapper')

# ---------------------------------------------------------------
# AIRBNB provider
# ---------------------------------------------------------------


def scrap_airbnb_data(id):
    try:
        api = airbnb.Api(
            randomize=True,
            api_key=settings.AIRBNB_API_KEY,
            currency="EUR",
            locale="fr",
            country="fr",
            language="fr-fr",
        )
        details = api.get_listing_details(id)
        reviews = api.get_reviews(id)

        # backup received data for debugging purpose
        if settings.USE_DEBUG_DATA_STORAGE:  # pragma: no cover
            save_debug_data(f"scrapper/{id}/details.json", details)
            save_debug_data(f"scrapper/{id}/reviews.json", reviews)

        return (details, reviews)
    except Exception:
        return None


def _get_airbnb_name(data):
    return data.get("p3_summary_title") if data else None


def _get_airbnb_host_info(data):
    if not data or "primary_host" not in data:
        return None

    host_data = data["primary_host"]
    return {
        "name": host_data.get("name"),
        "picture_url": host_data.get("picture_large_url"),
        "description": host_data.get("about"),
        "languages": host_data.get("languages"),
    }


def _get_airbnb_general_info(data):
    def _extract_count(value):
        v = re.split(r"\D+", value)[0] if value else None
        return v if v and v.isnumeric() else None

    return {
        "bathroom_count": _extract_count(data.get("bathroom_label")),
        "bed_count": _extract_count(data.get("bed_label")),
        "bedroom_count": _extract_count(data.get("bedroom_label")),
        "guest_count": _extract_count(data.get("guest_label")),
    } if data is not None else None


def _get_airbnb_location(data):
    return {
        "title": data.get("location_title"),
        "coords": {
            "lat": data.get("lat"),
            "lng": data.get("lng"),
        },
    } if data is not None else None


def _get_airbnb_photos(data):
    if not data or "photos" not in data:
        return None
    return [
        {
            "url": photo["large"].split("?")[0] if "large" in photo else None,
            "caption": photo.get("caption")
        }
        for photo in data["photos"]
    ]


def _get_airbnb_description(data):
    if not data or "sectioned_description" not in data or "description" not in data["sectioned_description"]:
        return None

    return data["sectioned_description"]["description"].split("\n")


def _get_airbnb_equipment_areas(data):
    return [
        {
            "name": area["title"],
            "equipments": [str(e) for e in area.get("amenity_ids", [])]
        }
        for area in data
        if all(x in area for x in ["title", "amenity_ids"]) and area["amenity_ids"]
    ] if data else []


def _get_airbnb_equipments(data):
    return {
        str(eq["id"]): {
            "name": eq["name"],
            "description": eq["description"]
        }
        for eq in data
        if all(x in eq for x in ["id", "name", "description"])
    } if data else {}


def _get_airbnb_equipments_per_area(data):
    if not data or any(x not in data or not data[x] for x in ["see_all_amenity_sections", "listing_amenities"]):
        return {}

    return {
        "areas": _get_airbnb_equipment_areas(data["see_all_amenity_sections"]),
        "equipments": _get_airbnb_equipments(data["listing_amenities"]),
    }


def _get_airbnb_reviews(data):
    def _to_date(d):
        return d.split("T")[0]

    return sorted(
        [
            {
                "author_name": review["author"]["first_name"],
                "author_picture_url": review["author"]["picture_url"],
                "review": review["comments"],
                "date": _to_date(review["created_at"]),
                "language": review["language"],
            }
            for review in data
            if all(x in review for x in ["author", "rating", "comments", "created_at", "language"])
            and all(x in review["author"] for x in ["has_profile_pic", "first_name", "picture_url"])
            and review["rating"] == 5
        ],
        key=lambda r: r["date"],
        reverse=True,
    )[:REVIEWS_COUNT] if data else []


def _get_airbnb_prices(data):
    return [
        {
            "label": price["label"],
            "value": price["value"],
        }
        for price in data.get("price_details", [])
        if all(x in price for x in ["label", "value"])
    ] if data else []


def _get_airbnb_highlights(data):
    return [
        {
            "headline": highlight["headline"],
            "message": highlight["message"]
        }
        for highlight in data.get("highlights", [])
        if all(x in highlight for x in ["headline", "message"])
    ] if data else []


def _get_airbnb_house_rules(data):
    if data and "guest_controls" in data and "structured_house_rules" in data["guest_controls"]:
        return data["guest_controls"]["structured_house_rules"]
    return []


def _get_airbnb_rooms(data):
    return [
        {
            "name": room["name_with_type"],
            "details": room["highlights_hometour"],
        }
        for room in data.get("hometour_rooms", [])
        if all(x in room for x in ["name_with_type", "highlights_hometour"])
    ] if data else []


def _validate_data(data):
    mandatory_fields = ["name", "description"]
    return data if data and all(data.get(f) for f in mandatory_fields) else None


def convert_airbnb_data(data):
    try:
        details, reviews = data
        details = details["pdp_listing_detail"]
        reviews = reviews["reviews"]

        data = {
            "name": _get_airbnb_name(details),
            "general_info": _get_airbnb_general_info(details),
            "host": _get_airbnb_host_info(details),
            "location": _get_airbnb_location(details),
            "photos": _get_airbnb_photos(details),
            "description": _get_airbnb_description(details),
            "equipments": _get_airbnb_equipments_per_area(details),
            "reviews": _get_airbnb_reviews(reviews),
            "prices": _get_airbnb_prices(details),
            "highlights": _get_airbnb_highlights(details),
            "house_rules": _get_airbnb_house_rules(details),
            "rooms": _get_airbnb_rooms(details),
        }
        return _validate_data(data)
    except Exception:
        return None


def scrap_and_convert(airbnb_id):
    _logger.info("scrap airbnb data {'id': %s}", airbnb_id)
    airbnb_data = scrap_airbnb_data(airbnb_id)
    if not airbnb_data:
        return None

    return convert_airbnb_data(airbnb_data)
