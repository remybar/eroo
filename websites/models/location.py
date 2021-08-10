from django.db import models

LOCATION_TITLE_LENGTH = 255


class WebsiteLocation(models.Model):
    title = models.CharField(max_length=LOCATION_TITLE_LENGTH)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.title
