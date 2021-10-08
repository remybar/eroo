from accounts.models import ErooUser

from .exceptions import InvalidUserType
from .models import CustomerSpace

def get_customer_space(user: ErooUser) -> CustomerSpace:
    if not user.is_owner:
        raise InvalidUserType("Only owners can have their own user spaces")

    space = user.customerspace_set.first()
    if not space:
        raise CustomerSpaceDoesNotExist(
            "Unable to find the customer space matching with the user (%s (%d))" % (user.email, user.id)
        )
    return space
