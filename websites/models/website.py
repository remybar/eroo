from shortuuid import ShortUUID

from django.conf import settings
from django.db import models
from django.utils import html
from django.core.files import File

from allauth.utils import get_user_model

from websites.config import MAX_WEBSITES_COUNT
from websites.utils import (
    get_filename_from_url,
    download_media_file,
    save_debug_data,
)
from .location import WebsiteLocation
from .photo import WebsitePhoto
from .review import Review
from .host import WebsiteHost
from .highlight import Highlight
from .room import Room, RoomDetail
from .rule import Rule
from .equipment import Equipment, EquipmentArea

User = get_user_model()

KEY_LENGTH = 16
NAME_LENGTH = 255

HOST_PICTURE_FILENAME = "host.jpg"
EXPECTED_DATA_KEYS = ["name", "description", "photos"]


class Website(models.Model):
    key = models.CharField(max_length=KEY_LENGTH)
    rental_url = models.URLField()
    name = models.CharField(max_length=NAME_LENGTH, default="")
    description = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)

    bedroom_count = models.IntegerField()
    bed_count = models.IntegerField()
    bathroom_count = models.IntegerField()
    guest_count = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(WebsiteLocation, on_delete=models.CASCADE)

    def __str__(self):
        return self.rental_url

    def _generate_key():
        """
        generate a key and be sure that it's truely unique (not yet existing in the database)
        """
        new_key = ShortUUID().random(length=KEY_LENGTH)
        if Website.objects.filter(key=new_key).count() > 0:
            return Website._generate_key()
        return new_key

    def _generate_description(desc_lines):
        """
        Generate the description based on the list of description lines.
        Basically, every line is surrounded by <p></p> tags except if it's an empty line.
        In that case, <br/> is used.
        """
        return "\n".join(
            [f"<p>{html.escape(line)}</p>" if line else "<br />" for line in desc_lines]
        )

    def _create_photo(self, filename, content, caption):
        photo = WebsitePhoto.objects.create(caption=caption, website=self)
        photo.image.save(filename, File(content))
        photo.save()

    def _create_photos(self, photos):
        for p in photos:
            if all(f in p for f in ["url", "caption"]):
                filename = get_filename_from_url(p["url"])
                photo_content = download_media_file(p["url"], filename)
                if photo_content:
                    self._create_photo(filename, photo_content, p["caption"])

    def _create_reviews(self, reviews):
        for r in reviews:
            filename = get_filename_from_url(r["author_picture_url"])
            media_file = download_media_file(r["author_picture_url"], filename)
            if media_file:
                review = Review(
                    author_name=r["author_name"],
                    review=r["review"],
                    date=r["date"],
                    language=r["language"],
                    website=self
                )
                review.save()
                review.author_picture.save(filename, File(media_file))
                review.save()

    def _create_location(location_data):
        location = WebsiteLocation(
            title=location_data["title"],
            latitude=location_data["coords"]["lat"],
            longitude=location_data["coords"]["lng"],
        )
        location.save()
        return location

    def _create_host(self, host_data):
        media_file = download_media_file(host_data["picture_url"], HOST_PICTURE_FILENAME)
        if media_file:
            host = WebsiteHost(
                name=host_data["name"],
                description=host_data["description"],
                languages=",".join(host_data["languages"]),
                website=self,
            )
            host.save()
            host.picture.save(HOST_PICTURE_FILENAME, File(media_file))

    def _create_equipments(self, equipment_data):
        # create equipments
        equipments = dict()
        for id, equipment in equipment_data["equipments"].items():
            equipments[id] = Equipment(
                name=equipment["name"], description=equipment["description"]
            )
            equipments[id].save()

        # create areas
        for area in equipment_data["areas"]:
            new_area = EquipmentArea(name=area["name"], website=self)
            new_area.save()
            for id in area["equipments"]:
                if id in equipments:
                    new_area.equipments.add(equipments[id])

    def _create_highlights(self, highlight_data):
        for h in highlight_data:
            Highlight(title=h["headline"], message=h["message"], website=self).save()

    def _create_rules(self, rules_data):
        for r in rules_data:
            Rule(name=r, website=self).save()

    def _create_rooms(self, rooms_data):
        for r in rooms_data:
            new_room = Room(name=r["name"], website=self)
            new_room.save()
            for d in r["details"]:
                RoomDetail(detail=d, room=new_room).save()

    def create(user_id, url, data):
        """create a new website based on data received from the scrapper"""

        # sanity checks
        if not all([k in data for k in EXPECTED_DATA_KEYS]):
            return False

        # create the website
        location = Website._create_location(data["location"])
        website = Website(
            key=Website._generate_key(),
            user=User.objects.get(id=user_id),
            rental_url=url,
            name=data["name"],
            description=Website._generate_description(data["description"]),
            guest_count=data["general_info"]["guest_count"],
            bedroom_count=data["general_info"]["bedroom_count"],
            bed_count=data["general_info"]["bed_count"],
            bathroom_count=data["general_info"]["bathroom_count"],
            location=location,
        )
        website.save()
        website._create_host(data["host"])
        website._create_photos(data["photos"])
        website._create_reviews(data["reviews"])
        website._create_equipments(data["equipments"])
        website._create_highlights(data["highlights"])
        website._create_rules(data["house_rules"])
        website._create_rooms(data["rooms"])

        # for debugging purpose, store data received from the scrapper
        if settings.USE_DEBUG_DATA_STORAGE:
            save_debug_data(f"api/{website.key}/api_data.json", data)

        return website

    def get_website(key):
        """ get the website record identified by `key` """
        try:
            return Website.objects.get(key=key)
        except Website.DoesNotExist:
            return None

    def has_reached_resource_limits(user):
        """ indicates if resource limits have been reached for the `user` """
        return Website.objects.filter(user=user).count() >= MAX_WEBSITES_COUNT
