from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from accounts.models import ErooUser
from .services import create_customer_space

@receiver(user_signed_up, sender=ErooUser)
def on_user_signed_up(sender, request, user, **kwargs):
    if  user.is_owner:
        create_customer_space(user=user)
