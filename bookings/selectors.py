from collections.abc import Sequence, Iterable
from datetime import date

from bookings.models.booking import (
    Housing,
    BookingSeason,
    BookingRateModifier,
    BookingPeriod,
    BookingPriceCategory,
    PeriodOfYear,
    BookingDate,
    BookingDateSet,
)
from bookings.exceptions import (
    UnexistingHousing,
    BookingSeasonNoMatchFound,
    UnexistingBookingSeason,
    UnexistingBookingPeriod,
    UnexistingBookingRateModifier,
    UnexistingBookingPriceCategory,
)
from bookings.utils import (
    Range,
    _intersect_two_ranges,
    _intersect_all,
)

def get_housing_list() -> Iterable[Housing]:
    """
    Get the list of available housings
    """
    return Housing.objects.all()

def get_housing(*, housing_id: int) -> Housing:
    """
    Get a housing with its id.
    """
    qs = Housing.objects.filter(pk=housing_id)
    if not qs:
        raise UnexistingHousing(f"The housing {housing_id} does not exist")
    return qs.first()

def get_booking_season_list() -> Iterable[BookingSeason]:
    """
    Get the list of booking seasons
    """
    return BookingSeason.objects.all()

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

def is_period_overlaps_another_one(
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

def explode_booking_dates_in_season_periods(*, housing: Housing, booking_date: BookingDate) -> dict:
    """
    As booking dates may overlap several seasons, this function split the period defined by booking dates into
    a dictionary of booking period per season.
    """
    seasons = BookingSeason.objects.filter(housing=housing)
    periods = BookingPeriod.objects.filter(season__in=seasons)

    result = {}
    for p in periods:
        dates_in_period = _intersect_two_ranges(
            range1=Range(booking_date.start, booking_date.end),
            range2=Range(p.start_period.to_date(), p.end_period.to_date())
        )
        if dates_in_period:
            if p.season.id in result:
                existing_dates = result[p.season.id].dates
                existing_nb_of_nights = result[p.season.id].nb_of_nights
            else:
                existing_dates = []
                existing_nb_of_nights = 0

            new_date = BookingDate(start=dates_in_period.start, end=dates_in_period.end)

            # compute the number of nights (by taking into account the fact that the end date is not
            # a real night but the date when travelers leave the place
            nb_of_nights = (new_date.end - new_date.start).days + (1 if new_date.end != booking_date.end else 0)

            result[p.season.id] = BookingDateSet(
                season=p.season,
                nb_of_nights=existing_nb_of_nights + nb_of_nights,
                dates=(*existing_dates, new_date)
            )

    return result
