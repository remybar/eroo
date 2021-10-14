from collections.abc import Sequence
from datetime import date

from bookings.models.booking import (
    Housing,
    BookingSeason,
    BookingRateModifier,
    BookingPeriod,
    BookingPriceCategory,
    PeriodOfYear,
)
from bookings.exceptions import (
    UnexistingBookingSeason,
    UnexistingBookingPeriod,
    UnexistingBookingRateModifier,
    UnexistingBookingPriceCategory,
)
from bookings.utils import Range, _intersect_all

def get_booking_season(*, season_id: int) -> BookingSeason:
    """
    Get a booking season with its id.
    """
    qs = BookingSeason.objects.filter(pk=season_id)
    if not qs:
        raise UnexistingBookingSeason(f"The season {season_id} does not exist")
    return qs.first()

def get_booking_rate_modifier(*, modifier_id: int) -> BookingRateModifier:
    """
    Get a booking rate modifier with its id.
    """
    qs = BookingRateModifier.objects.filter(pk=modifier_id)
    if not qs:
        raise UnexistingBookingRateModifier(f"The modifier {modifier_id} does not exist")
    return qs.first()

def get_booking_period(*, period_id: int) -> BookingPeriod:
    """
    Get a booking period with its id.
    """
    qs = BookingPeriod.objects.filter(pk=period_id)
    if not qs:
        raise UnexistingBookingPeriod(f"The period {period_id} does not exist")
    return qs.first()

def get_booking_price_category(*, category_id: int) -> BookingPriceCategory:
    """
    Get a booking price category with its id.
    """
    qs = BookingPriceCategory.objects.filter(pk=category_id)
    if not qs:
        raise UnexistingBookingPriceCategory(f"The category {category_id} does not exist")
    return qs.first()

def _is_period_overlaps_another_one(
    *, housing: Housing, start_period: PeriodOfYear, end_period: PeriodOfYear, exclude_ids: Sequence[int] = None
) -> bool:
    """
    Indicate if the period passed as parameter overlaps at least an existing period
    """
    seasons = BookingSeason.objects.filter(housing=housing)
    periods = BookingPeriod.objects.filter(season__in=seasons)
    if exclude_ids:
        periods = periods.exclude(id__in=exclude_ids)

    return _intersect_all(
        input_range=Range(start=start_period, end=end_period),
        ranges=[Range(start=p.start_period, end=p.end_period) for p in periods]
    )
