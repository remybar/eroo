from django.conf import settings
from django.core.management.base import BaseCommand
from accounts.models import ErooUser

from tenant_users.tenants.tasks import provision_tenant
from tenant_users.tenants.utils import create_public_tenant


class Command(BaseCommand):
    help = "setup the public tenant for eroo.fr"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        create_public_tenant(f"www.{settings.TENANT_USERS_DOMAIN}", "public@eroo.fr")
        ErooUser.objects.create_superuser(email="admin", password='admin', is_active=True)  # TODO: get the password from somewhere else

        # ErooUser.objects.create_user(email="tenant1@example.com", password='password', is_active=True, is_staff=True)
        # provision_tenant("Tenant1", "tenant1", "tenant1@example.com", is_staff=True)

        # ErooUser.objects.create_user(email="tenant2@example.com", password='password', is_active=True, is_staff=True)
        # provision_tenant("Tenant2", "tenant2", "tenant2@example.com", is_staff=True)
        print('Done')



