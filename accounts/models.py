from django.db import models
from django.contrib.auth.models import AbstractUser


class ErooUser(AbstractUser):
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return self.username
