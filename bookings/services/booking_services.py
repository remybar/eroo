from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import ErooUser
from bookings.models import Housing, Booking

class BookingAlreadyExists(Exception):
    pass

def _check_dates(start_date: datetime, end_date: datetime):
    """
    Check start/end dates consistency.
    """
    if start_date < timezone.now():
        raise ValidationError("The start date cannot be before today")

    if end_date < start_date:
        raise ValidationError("The end date must be after the start date")

def add_booking_season(*, housing: Housing, name: str, start_date: datetime, end_date: datetime) -> bool:
    """
    Add a new booking season.
    """
    _check_dates(start_date=start_date, end_date=end_date)


def compute_price(*, start_date: datetime, end_date: datetime, travelers_count: int) -> int:
    """
    Compute the price for a given period of time and a number of travelers
    """
    _check_dates(start_date=start_date, end_date=end_date)

    # TODO return a price
    return travelers_count * 10


def book(*, user: ErooUser, start_date: datetime, end_date: datetime, travelers_count: int) -> str:
    """
    Book a housing from `start_date` to `end_date`, for `travelers_count` people.
    returns a booking reference or raise an exception.
    """
    _check_dates(start_date=start_date, end_date=end_date)

    if Booking.objects.filter(start_date=start_date, end_date=end_date):
        raise BookingAlreadyExists()

    return Booking.objects.create(
        start_date=start_date,
        end_date=end_date,
    )

# give_identity()
# def pay()
# def cancel()
