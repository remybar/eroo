from django.db import models

from websites.utils import get_photo_dir_path

CAPTION_LENGTH = 255


class WebsitePhoto(models.Model):
    image = models.ImageField(upload_to=get_photo_dir_path)
    website = models.ForeignKey("websites.Website", on_delete=models.CASCADE)
    caption = models.CharField(max_length=CAPTION_LENGTH)

    def __str__(self):
        return self.image.name

    def url(self):
        return self.image.url
