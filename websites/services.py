import logging
import re
import requests
from typing import Union, Sequence, Any

from django.conf import settings
from django.core.files import File
from django.utils import html

from allauth.utils import get_user_model

from scrapper.services import scrap_and_convert
from bookings.models import Housing
from common.services import (
    get_filename_from_url,
    download_media_file,
    save_debug_data,
)
from websites.config import HOST_PICTURE_FILENAME, EXPECTED_AIRBNB_DATA_KEYS
from websites.models import (
    Website,
    WebsiteLocation,
    WebsiteHost,
    WebsitePhoto,
    Equipment,
    EquipmentArea,
    Highlight,
    Review,
    Room,
    RoomDetail,
    Rule,
)
from websites.selectors import generate_website_key

User = get_user_model()

_logger = logging.getLogger(__name__)

def _explode_airbnb_url(*, url: str) -> tuple:
    """
    From a raw airbnb URL (might be an alias), returns the base airbnb URL
    such as https://airbnb.fr/rooms/12345 and the airbnb_id
    """
    def _explode(_url):
        base_url = _url.split("?")[0]
        res = re.search(r"/([0-9]+)$", base_url)
        if res:
            return (base_url, res.group(1))
        return None, None

    try:
        base_url, airbnb_id = _explode(url)
        if not airbnb_id:
            # the provided url main be a shortcut of the real airbnb URL
            # in this case, just access to the URL to retrieve the real URL
            response = requests.get(url, timeout=1)
            if response.status_code != 200:
                return None, None
            base_url, airbnb_id = _explode(response.url)
    except Exception:
        return None, None

    return base_url, airbnb_id

def _are_airbnb_data_valid(*, data: dict) -> bool:
    """
    check that all expected items in the airbnb data dict are present.
    """
    return all([k in data for k in EXPECTED_AIRBNB_DATA_KEYS])

def create_location(*, website: Website, data: dict):
    """
    Create a location record from airbnb data.
    """
    location = WebsiteLocation.objects.create(
        title=data["title"],
        latitude=data["coords"]["lat"],
        longitude=data["coords"]["lng"],
    )
    website.location = location
    website.save(update_fields=["location"])

def create_equipments(*, website=Website, data: dict):
    """
    Create equipments and equipment areas records from airbnb data.
    """
    equipments = dict()
    for id, equipment in data["equipments"].items():
        equipments[id] = Equipment.objects.create(
            name=equipment["name"],
            description=equipment["description"],
        )
    for area in data["areas"]:
        new_area = EquipmentArea.objects.create(name=area["name"], website=website)
        for id in area["equipments"]:
            if id in equipments:
                new_area.equipments.add(equipments[id])

def create_highlights(*, website=Website, data: dict):
    """
    Create highlight records from airbnb data.
    """
    for h in data:
        Highlight.objects.create(title=h["headline"], message=h["message"], website=website)

def create_rules(*, website=Website, data: dict):
    """
    Create rule records from airbnb data.
    """
    for r in data:
        Rule.objects.create(name=r, website=website)

def create_rooms(*, website=Website, data: dict):
    for r in data:
        new_room = Room.objects.create(name=r["name"], website=website)
        for d in r["details"]:
            RoomDetail.objects.create(detail=d, room=new_room)

def create_reviews(*, website=Website, data: dict):
    for r in data:
        filename = get_filename_from_url(r["author_picture_url"])
        media_file = download_media_file(r["author_picture_url"], filename)
        if media_file:
            review = Review.objects.create(
                author_name=r["author_name"],
                review=r["review"],
                date=r["date"],
                language=r["language"],
                website=website,
            )
            review.author_picture.save(filename, File(media_file))
            review.save()

def _create_photo(*, website: Website, filename: str, content: Any, caption: str):
    photo = WebsitePhoto.objects.create(caption=caption, website=website)
    photo.image.save(filename, File(content))
    photo.save()

def create_photos(*, website=Website, data: dict):
    """
    Download and create photo records from airbnb data.
    """
    for p in data:
        if all(f in p for f in ["url", "caption"]):
            filename = get_filename_from_url(p["url"])
            photo_content = download_media_file(p["url"], filename)
            if photo_content:
                _create_photo(website=website, filename=filename, content=photo_content, caption=p["caption"])

def create_host(*, website: Website, data: dict):
    """
    Create a host record from airbnb data.
    """
    media_file = download_media_file(data["picture_url"], HOST_PICTURE_FILENAME)
    if media_file:
        host = WebsiteHost.objects.create(
            name=data["name"],
            description=data["description"],
            languages=",".join(data["languages"]),
            website=website,
        )
        host.picture.save(HOST_PICTURE_FILENAME, File(media_file))

def _generate_website_description(*, desc_lines: Sequence[str]) -> str:
    """
    Generate the description based on the list of description lines.
    Basically, every line is surrounded by <p></p> tags except if it's an empty line.
    In that case, <br/> is used.
    """
    return "\n".join(
        [f"<p>{html.escape(line)}</p>" if line else "<br />" for line in desc_lines]
    )

def create_website(*, user: User, housing: Housing, data: dict) -> Website:
    """
    Create a website record from airbnb data.
    """
    return Website.objects.create(
        key=generate_website_key(),
        user=user,
        housing=housing,
        name=data["name"],
        description=_generate_website_description(data["description"]),
        guest_count=data["general_info"]["guest_count"],
        bedroom_count=data["general_info"]["bedroom_count"],
        bed_count=data["general_info"]["bed_count"],
        bathroom_count=data["general_info"]["bathroom_count"],
    )

def create_website_structure(*, user: User, housing: Housing, data: dict) -> Website:
    """
    create the whole website structure from scrapped data
    """
    if not _are_airbnb_data_valid(data=data):
        return False

    website = create_website(user=user, housing=Housing, data=data)

    create_location(website=website, data=data["location"])
    create_host(website=website, data=data["host"])
    create_photos(website=website, data=data["photos"])
    create_reviews(website=website, data=data["reviews"])
    create_equipments(website=website, data=data["equipments"])
    create_highlights(website=website, data=data["highlights"])
    create_rules(website=website, data=data["house_rules"])
    create_rooms(website=website, data=data["rooms"])

    # for debugging purpose, store data received from the scrapper
    if settings.USE_DEBUG_DATA_STORAGE:
        save_debug_data(f"api/{website.key}/api_data.json", data)

    return website

def generate_website_from_airbnb(*, user: User, housing: Housing):
    """
    Generate a website and all its attributes for a specific housing.
    """
    _, airbnb_id = _explode_airbnb_url(url=housing.airbnb_url)

    _logger.info("scrap and create website for {'airbnb_id': %s}", airbnb_id)
    try:
        scrapped_data = scrap_and_convert(airbnb_id=airbnb_id)
    except Exception:
        scrapped_data = None

    if not scrapped_data:
        return {
            "result": "error",
            "msg": "Impossible d'accéder à votre annonce Airbnb"
        }

    # generate the website and get the redirect page
    try:
        website = create_website_structure(user=user, housing=housing, data=scrapped_data)
    except Exception as e:
        _logger.exception(str(e))
        website = None

    if not website:
        return {
            "result": "error",
            "msg": "Impossible de créer le site web à partir des données de votre annonce"
        }

    # TODO BAR: dois-je retourner tout ça ?
    # return {
    #     "result": "success",
    #     "key": website.key,
    #     "name": website.name,
    #     "url": WEBSITE_URL % website.key,
    #     "generated_date": defaultfilters.date(timezone.localtime(website.generated_date), "d/m/Y G:i"),
    #     "delete_url": reverse('api_website_delete', args=[website.key]),
    # }
