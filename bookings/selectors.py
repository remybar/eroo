from collections.abc import Sequence
from datetime import date

from bookings.models.booking import Housing, BookingSeason, BookingPeriod
from bookings.exceptions import UnexistingBookingSeason, UnexistingBookingPeriod
from bookings.utils import Range, _intersect_all

def get_booking_season(*, season_id: int) -> BookingSeason:
    """
    Get a booking season with its id.
    """
    qs = BookingSeason.objects.filter(pk=season_id)
    if not qs:
        raise UnexistingBookingSeason(f"The season {season_id} does not exist")
    return qs.first()

def get_booking_period(*, period_id: int) -> BookingPeriod:
    """
    Get a booking period with its id.
    """
    qs = BookingPeriod.objects.filter(pk=period_id)
    if not qs:
        raise UnexistingBookingPeriod(f"The period {period_id} does not exist")
    return qs.first()

def _is_period_overlaps_another_one(
    *, housing: Housing, start_date: date, end_date: date, exclude_ids: Sequence[int] = None
) -> bool:
    """
    Indicate if the period passed as parameter overlaps at least an existing period
    """
    seasons = BookingSeason.objects.filter(housing=housing)
    periods = BookingPeriod.objects.filter(season__in=seasons)
    if exclude_ids:
        periods = periods.exclude(id__in=exclude_ids)

    return _intersect_all(
        input_range=Range(start=start_date, end=end_date),
        ranges=[Range(start=p.start_date, end=p.end_date) for p in periods]
    )
