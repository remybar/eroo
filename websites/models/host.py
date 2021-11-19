from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from websites.models.common import get_photo_dir_path


HOST_NAME_LENGTH = 64
HOST_LANGUAGES_LENGTH = 255


class WebsiteHost(models.Model):
    name = models.CharField(max_length=HOST_NAME_LENGTH)
    description = models.TextField()
    languages = models.CharField(max_length=HOST_LANGUAGES_LENGTH)
    website = models.ForeignKey("websites.Website", on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_photo_dir_path)

    def __str__(self):
        return self.name

    def picture_url(self):
        return self.picture.url


@receiver(pre_delete, sender=WebsiteHost)
def delete_host(sender, instance, **kwargs):
    if instance.picture:
        instance.picture.delete(save=False)
