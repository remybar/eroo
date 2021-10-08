from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from tenant_users.tenants.tasks import provision_tenant

from accounts.models import ErooUser

from .exceptions import InvalidUserType

def create_customer_space(*, user: ErooUser) -> bool:
    """
    Create a new customer space ()
    """
    if not user.is_owner:
        raise InvalidUserType("Only owners can have their own user spaces")

    fqdn = provision_tenant(
        tenant_name=user.username,
        tenant_slug=user.spacename,
        user_email=user.email,
    )
