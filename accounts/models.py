from django.db import models
from tenant_users.tenants.models import UserProfile

class ErooUser(UserProfile):
    username = models.CharField(max_length=32)
    is_owner = models.BooleanField(default=False)
    spacename = models.CharField(max_length=32, blank=True, null=True)

    """
    A global user on the Eroo platform
    """
    def __str__(self):
        return f"{self.username} ({self.email})"
