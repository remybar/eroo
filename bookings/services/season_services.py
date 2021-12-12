from collections import namedtuple
from datetime import date
from typing import Union

from django.core.exceptions import ValidationError
from django.utils import timezone

from allauth.utils import get_user_model

from bookings.exceptions import (
    UnexistingBookingSeason,
    BookingPeriodOverlapping,
)
from bookings.models import (
    Housing,
    BookingSeason,
    BookingRateModifier,
    BookingPeriod,
    Weekdays,
    PeriodOfYear,
)
from websites.tasks import task_generate_website_from_airbnb
from bookings.selectors import (
    get_housing,
    is_period_overlaps_another_one,
    get_booking_season,
    get_booking_rate_modifier,
    get_booking_period,
)
from bookings.utils import _check_dates

User = get_user_model()

def create_housing(*, user: User, name: str, airbnb_url: str) -> Housing:

    # TODO BAR: raise an exception if the limit is reached

    housing = Housing.objects.create(
        user=user,
        name=name,
        airbnb_url=airbnb_url,
    )
    res = task_generate_website_from_airbnb.delay(
        user_id=user.id,
        housing_id=housing.id,
    ) if housing else False

    housing.website_task_id = res.id
    housing.save(update_fields=["website_task_id"])
    return housing

def update_housing(*, housing_id: int, name: str) -> Housing:
    housing = get_housing(housing_id=housing_id)
    housing.name = name
    housing.save(update_fields=["name"])
    return housing

def delete_housing(*, housing_id: int) -> None:
    housing = get_housing(housing_id=housing_id)
    housing.delete()

def create_booking_season(*, housing: Housing, name: str) -> BookingSeason:
    """
    Create a new booking season.
    """
    return BookingSeason.objects.create(housing=housing, name=name)

def update_booking_season(*, season_id: int, new_name: str) -> BookingSeason:
    """
    Update a booking season
    """
    season = get_booking_season(season_id=season_id)
    season.name = new_name
    season.save(update_fields=["name"])
    return season

def delete_booking_season(*, season_id: int) -> None:
    """
    Delete a booking season
    """
    season = get_booking_season(season_id=season_id)
    season.delete()

def set_season_base_price(*, season_id: int, base_price: float) -> None:
    """
    Set the base price for the season
    """
    season = get_booking_season(season_id=season_id)
    season.base_price = base_price
    season.save(update_fields=["base_price"])

def add_season_rate_modifier(
    *, season_id: int, name: str, value: float, nb_of_days: int, is_percent: bool = True, is_discount: bool = True,
    weekdays: Weekdays = None
) -> BookingRateModifier:
    """
    Add a rate modifier on the season (will be applied on the base price)
    """
    season = get_booking_season(season_id=season_id)
    weekdays = Weekdays() if not weekdays else weekdays

    return BookingRateModifier.objects.create(
        season=season,
        name=name,
        value=value,
        is_percent=is_percent,
        is_discount=is_discount,
        minimal_number_of_days=nb_of_days,
        monday=weekdays.mon,
        tuesday=weekdays.tue,
        wednesday=weekdays.wed,
        thursday=weekdays.thu,
        friday=weekdays.fri,
        saturday=weekdays.sat,
        sunday=weekdays.sun,
    )

def update_season_rate_modifier(
    *, modifier_id: int, name: str, value: float, nb_of_days: int, is_percent: bool, is_discount: bool,
    weekdays: Weekdays
) -> BookingRateModifier:
    """
    Update an existing rate modifier.
    """
    modifier = get_booking_rate_modifier(modifier_id=modifier_id)
    modifier.name = name
    modifier.value = value
    modifier.minimal_number_of_days = nb_of_days
    modifier.is_percent = is_percent
    modifier.is_discount = is_discount
    modifier.weekdays = weekdays
    modifier.save()

    return modifier

def delete_season_rate_modifier(*, modifier_id: int) -> None:
    """
    Remove a rate modifier.
    """
    modifier = get_booking_rate_modifier(modifier_id=modifier_id)
    modifier.delete()

def add_booking_season_period(*, season_id: int, start_period: PeriodOfYear, end_period: PeriodOfYear) -> BookingPeriod:
    """
    Add a new period to a season
    """
    PeriodOfYear.check_range(start_period, end_period)

    season = get_booking_season(season_id=season_id)
    if is_period_overlaps_another_one(housing=season.housing, start_period=start_period, end_period=end_period):
        raise BookingPeriodOverlapping("the new period overlaps at least another existing period.")

    return BookingPeriod.objects.create(
        season=season, _start_date=start_period.to_date(), _end_date=end_period.to_date()
    )

def update_booking_season_period(
    *, period_id: int, start_period: PeriodOfYear, end_period: PeriodOfYear
) -> BookingPeriod:
    """
    Update an existing booking period
    """
    PeriodOfYear.check_range(start_period, end_period)

    period = get_booking_period(period_id=period_id)
    if is_period_overlaps_another_one(
        housing=period.season.housing, start_period=start_period, end_period=end_period, exclude_ids=[period.id]
    ):
        raise BookingPeriodOverlapping("the new period overlaps at least another existing period.")

    period.start_period = start_period
    period.end_period = end_period
    period.save()

    return period

def delete_booking_season_period(*, period_id: int) -> None:
    """
    Remove an existing booking period
    """
    period = get_booking_period(period_id=period_id)
    period.delete()
