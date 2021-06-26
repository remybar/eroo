import logging
from shortuuid import ShortUUID

from django.conf import settings
from django.db import models
from django.utils import html

from allauth.utils import get_user_model

from .utils import (
    get_filename_from_url,
    download_media_files,
    download_media_file,
    save_debug_data
)

logger = logging.getLogger(__name__)


KEY_LENGTH = 16
NAME_LENGTH = 255
PHOTO_FILENAME_LENGTH = 128
LOCATION_TITLE_LENGTH = 255
AUTHOR_NAME_LENGTH = 64
AUTHOR_PICTURE_FILENAME_LENGTH = 128
LANGUAGE_LENGTH = 8
CAPTION_LENGTH = 255
EQUIPMENT_NAME_LENGTH = 128
EQUIPMENT_AREA_NAME_LENGTH = 128
HIGHLIGHT_TITLE_LENGTH = 255
RULE_NAME_LENGTH = 255

HOST_NAME_LENGTH = 64
HOST_PICTURE_FILENAME_LENGTH = 128
HOST_LANGUAGES_LENGTH = 255

HOST_PICTURE_FILENAME = "host.jpg"

EXPECTED_DATA_KEYS = ["name", "description", "photos"]


def _get_photo_dir_path(instance, filename):
    return f"websites/{instance.website.key}/photos/{filename}"


def _get_review_dir_path(instance, filename):
    return f"websites/{instance.website.key}/reviews/{filename}"


class WebsiteLocation(models.Model):
    title = models.CharField(max_length=LOCATION_TITLE_LENGTH)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.title


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

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
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

    def _create_photos(self, photos):
        photos_infos = []
        for p in photos:
            photo = WebsitePhoto(caption=p["caption"], website=self)
            photo.save()
            photos_infos.append((p["url"], get_filename_from_url(p["url"]), photo.image, photo))
        download_media_files(photos_infos)

    def _create_reviews(self, reviews):
        review_infos = []
        for r in reviews:
            review = Review(
                author_name=r["author_name"],
                review=r["review"],
                date=r["date"],
                language=r["language"],
                website=self
            )
            review.save()
            review_infos.append((
                r["author_picture_url"],
                get_filename_from_url(r["author_picture_url"]),
                review.author_picture,
                review
            ))
        download_media_files(review_infos)

    def _create_location(location_data):
        location = WebsiteLocation(
            title=location_data["title"],
            latitude=location_data["coords"]["lat"],
            longitude=location_data["coords"]["lng"],
        )
        location.save()
        return location

    def _create_host(self, host_data):
        host = WebsiteHost(
            name=host_data["name"],
            description=host_data["description"],
            languages=",".join(host_data["languages"]),
            website=self,
        )
        host.save()
        logger.info("VALUE OF USE_S3: %s", settings.USE_S3)
        download_media_file((host_data["picture_url"], HOST_PICTURE_FILENAME, host.picture, host))

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

    def create(user, url, data):
        """create a new website based on data received from the scrapper"""

        # sanity checks
        if not all([k in data for k in EXPECTED_DATA_KEYS]):
            return False

        # create the website
        location = Website._create_location(data["location"])
        website = Website(
            key=Website._generate_key(),
            user=user,
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


class WebsiteHost(models.Model):
    name = models.CharField(max_length=HOST_NAME_LENGTH)
    description = models.TextField()
    languages = models.CharField(max_length=HOST_LANGUAGES_LENGTH)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=_get_photo_dir_path)

    def __str__(self):
        return self.name

    def picture_url(self):
        return self.picture.url


class WebsitePhoto(models.Model):
    image = models.ImageField(upload_to=_get_photo_dir_path)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    caption = models.CharField(max_length=CAPTION_LENGTH)

    def __str__(self):
        return self.image.name

    def url(self):
        return self.image.url


class Review(models.Model):
    author_name = models.CharField(max_length=AUTHOR_NAME_LENGTH)
    author_picture = models.ImageField(upload_to=_get_review_dir_path)
    review = models.TextField()
    date = models.DateField()
    language = models.CharField(max_length=LANGUAGE_LENGTH)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author_name} ({self.date})"

    def picture_url(self):
        return self.author_picture.url


class Equipment(models.Model):
    name = models.CharField(max_length=EQUIPMENT_NAME_LENGTH)
    description = models.TextField()

    def __str__(self):
        return self.name


class EquipmentArea(models.Model):
    name = models.CharField(max_length=EQUIPMENT_AREA_NAME_LENGTH)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    equipments = models.ManyToManyField(Equipment)

    def __str__(self):
        return self.name


class Highlight(models.Model):
    title = models.CharField(max_length=HIGHLIGHT_TITLE_LENGTH)
    message = models.TextField()
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Rule(models.Model):
    name = models.CharField(max_length=RULE_NAME_LENGTH)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=RULE_NAME_LENGTH)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RoomDetail(models.Model):
    detail = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"detail of {self.room.name}"
