from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from allauth.utils import get_user_model

from bookings.models import Housing
from common.services import delete_debug_data

from websites.models.location import WebsiteLocation
from websites.slots import on_delete_website


User = get_user_model()

KEY_LENGTH = 16
NAME_LENGTH = 255

class Website(models.Model):
    key = models.CharField(max_length=KEY_LENGTH)
    name = models.CharField(max_length=NAME_LENGTH, default="")
    description = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)

    bedroom_count = models.IntegerField()
    bed_count = models.IntegerField()
    bathroom_count = models.IntegerField()
    guest_count = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(WebsiteLocation, on_delete=models.CASCADE)
    housing = models.OneToOneField(Housing, on_delete=models.CASCADE, related_name="website")

    def __str__(self):
        return f"{self.name} (key: {self.key})"

@receiver(pre_delete, sender=Website)
def delete_website(sender, instance, **kwargs):
    on_delete_website(airbnb_id=instance.housing.airbnb_id, website_key=instance.key)
