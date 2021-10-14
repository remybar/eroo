from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import ErooUser
from bookings.exceptions import (
    BookingSeasonNoMatchFound,
)
from bookings.models import (
    Housing,
    Booking,
)

class BookingAlreadyExists(Exception):
    pass

def compute_price(*, start_date: date, end_date: date) -> int:
    """
    Compute the price for a given period of time
    """
    _check_period_range(start_date=start_date, end_date=end_date)

    raise BookingSeasonNoMatchFound(
        "No season matches the period of time (%s - %s) " % (
            start_date.strftime("%d-%m-%Y"),
            end_date.strftime("%d-%m-%Y"),
        )
    )

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
