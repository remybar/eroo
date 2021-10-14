from bookings.models import (
    Housing,
    BookingPriceCategory,
)
from bookings.selectors import (
    get_booking_price_category,
)

def add_price_category(*, housing: Housing, name: str) -> BookingPriceCategory:
    """
    Add a new price category (such as "Adult", "Child"...)
    """
    return BookingPriceCategory.objects.create(housing=housing, name=name)

def update_price_category(*, category_id: int, new_name: str) -> BookingPriceCategory:
    """
    Update a price category
    """
    category = get_booking_price_category(category_id=category_id)

    category.name = new_name
    category.save(update_fields=["name"])
    return category

def delete_price_category(*, category_id: int) -> None:
    """
    Remove a price category
    """
    category = get_booking_price_category(category_id=category_id)
    category.delete()
