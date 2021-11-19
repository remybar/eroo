from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from websites.models.common import get_photo_dir_path

CAPTION_LENGTH = 255


class WebsitePhoto(models.Model):
    image = models.ImageField(upload_to=get_photo_dir_path)
    website = models.ForeignKey("websites.Website", on_delete=models.CASCADE)
    caption = models.CharField(max_length=CAPTION_LENGTH)

    def __str__(self):
        return self.image.name

    def url(self):
        return self.image.url

@receiver(pre_delete, sender=WebsitePhoto)
def delete_photo(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
