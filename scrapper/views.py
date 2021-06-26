import airbnb
import json
import logging

from django.conf import settings

from websites.utils import save_debug_data

REVIEWS_COUNT = 5

_logger = logging.getLogger('scrapper')

# ---------------------------------------------------------------
# AIRBNB provider
# ---------------------------------------------------------------


def _scrap_airbnb_data(id):
    if settings.SCRAPPER_USE_FAKE_FILES:
        fake_data_path = settings.BASE_DIR / "scrapper" / "fake_data"
        with open(fake_data_path / "details.json") as f:
            details = json.load(f)
        with open(fake_data_path / "reviews.json") as f:
            reviews = json.load(f)
        return (details, reviews)

    try:
        # TODO: update the API token regularly ?
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
        if settings.USE_DEBUG_DATA_STORAGE:
            save_debug_data(f"scrapper/{id}/details.json", details)
            save_debug_data(f"scrapper/{id}/reviews.json", reviews)

        return (details, reviews)
    except Exception as e:
        _logger.error("Unable to scrap data {'exception': %s}", str(e))
        pass

    return False


def _get_airbnb_name(data):
    return data["p3_summary_title"]


def _get_airbnb_host_info(data):
    host_data = data["primary_host"]
    return {
        "name": host_data["name"],
        "picture_url": host_data["picture_large_url"],
        "description": host_data["about"],
        "languages": host_data["languages"],
    }


def _get_airbnb_general_info(data):
    def _extract_count(value):
        return int(value.split()[0].split(",")[0].split(".")[0])

    return {
        "bathroom_count": _extract_count(data["bathroom_label"]),
        "bed_count": _extract_count(data["bed_label"]),
        "bedroom_count": _extract_count(data["bedroom_label"]),
        "guest_count": _extract_count(data["guest_label"]),
    }


def _get_airbnb_location(data):
    return {
        "title": data["location_title"],
        "coords": {
            "lat": data["lat"],
            "lng": data["lng"],
        },
    }


def _get_airbnb_photos(data):
    return [
        {"url": photo["large"].split("?")[0], "caption": photo["caption"]}
        for photo in data["photos"]
    ]


def _get_airbnb_description(data):
    return data["sectioned_description"]["description"].split("\n")


def _get_airbnb_equipments(data):
    return {
        "equipments": {
            equipment["id"]: {
                "name": equipment["name"],
                "description": equipment["description"],
            }
            for equipment in data["listing_amenities"]
        },
        "areas": [
            {
                "name": area["title"],
                "equipments": [str(id) for id in area["amenity_ids"]],
            }
            for area in data["see_all_amenity_sections"]
        ],
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
            if review["author"]["has_profile_pic"] and review["rating"] == 5
        ],
        key=lambda r: r["date"],
        reverse=True,
    )[:REVIEWS_COUNT]


def _get_airbnb_prices(data):
    return [
        {
            "label": price["label"],
            "value": price["value"],
        }
        for price in data["price_details"]
    ]


def _get_airbnb_highlights(data):
    return [
        {"headline": highlight["headline"], "message": highlight["message"]}
        for highlight in data["highlights"]
    ]


def _get_airbnb_house_rules(data):
    return data["guest_controls"]["structured_house_rules"]


def _get_airbnb_rooms(data):
    return [
        {
            "name": room["name_with_type"],
            "details": room["highlights_hometour"],
        }
        for room in data["hometour_rooms"]
    ]


def _convert_airbnb_data(data):
    try:
        details, reviews = data
        details = details["pdp_listing_detail"]
        reviews = reviews["reviews"]

        return {
            "name": _get_airbnb_name(details),
            "general_info": _get_airbnb_general_info(details),
            "host": _get_airbnb_host_info(details),
            "location": _get_airbnb_location(details),
            "photos": _get_airbnb_photos(details),
            "description": _get_airbnb_description(details),
            "equipments": _get_airbnb_equipments(details),
            "reviews": _get_airbnb_reviews(reviews),
            "prices": _get_airbnb_prices(details),
            "highlights": _get_airbnb_highlights(details),
            "house_rules": _get_airbnb_house_rules(details),
            "rooms": _get_airbnb_rooms(details),
        }
    except Exception as e:
        _logger.error("Unable to convert scrapped data {'exception': %s}", str(e))
        return False


def scrap_airbnb_data(airbnb_id):
    _logger.info("scrap airbnb data {'id': %s}", airbnb_id)
    airbnb_data = _scrap_airbnb_data(airbnb_id)
    if not airbnb_data:
        return False

    api_data = _convert_airbnb_data(airbnb_data)
    if not api_data:
        return False

    return api_data
