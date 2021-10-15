from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import ErooUser
from bookings.exceptions import (
    BookingSeasonNoMatchFound,
    BookingAlreadyExists,
)
from bookings.models import (
    Housing,
    Booking,
    BookingDate,
)
from bookings.selectors import (
    explode_booking_dates_in_season_periods,
)
from bookings.utils import _check_dates

def _compute_base_price(season_periods, booking_date: BookingDate) -> int:
    """
    Parse season periods to compute the base price.
    """
    return sum(
        nb_of_nights * season.base_price
        for season_id, (season, nb_of_nights, _) in season_periods.items()
    )

def compute_price(*, housing: Housing, booking_date: BookingDate) -> int:
    """
    Compute the price for a given period of time
    """
    _check_dates(booking_date)

    season_periods = explode_booking_dates_in_season_periods(housing=housing, booking_date=booking_date)
    if not season_periods:
        raise BookingSeasonNoMatchFound("No season matching the booking dates has been found")

    return _compute_base_price(season_periods=season_periods, booking_date=booking_date)


# def book(*, user: ErooUser, start_date: datetime, end_date: datetime, travelers_count: int) -> str:
#     """
#     Book a housing from `start_date` to `end_date`, for `travelers_count` people.
#     returns a booking reference or raise an exception.
#     """
#     _check_dates(start_date=start_date, end_date=end_date)

#     if Booking.objects.filter(start_date=start_date, end_date=end_date):
#         raise BookingAlreadyExists()

#     return Booking.objects.create(
#         start_date=start_date,
#         end_date=end_date,
#     )

# give_identity()
# def pay()
# def cancel()
