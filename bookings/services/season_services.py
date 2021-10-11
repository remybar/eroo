from datetime import date
from typing import Union

from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import ErooUser
from bookings.exceptions import UnexistingBookingSeason, BookingPeriodOverlapping
from bookings.models import Housing, BookingSeason, BookingPeriod
from bookings.selectors import (
    _is_period_overlaps_another_one,
    get_booking_season,
    get_booking_period,
)
from bookings.utils import _check_dates

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

def add_booking_season_period(*, season_id: int, start_date: date, end_date: date) -> BookingPeriod:
    """
    Add a new period to a season
    """
    _check_dates(start_date, end_date)

    season = get_booking_season(season_id=season_id)
    if _is_period_overlaps_another_one(housing=season.housing, start_date=start_date, end_date=end_date):
        raise BookingPeriodOverlapping("the new period overlaps at least another existing period.")

    return BookingPeriod.objects.create(
        season=season, start_date=start_date, end_date=end_date
    )

def update_booking_season_period(*, period_id: int, start_date: date, end_date: date) -> BookingPeriod:
    """
    Update an existing booking period
    """
    _check_dates(start_date, end_date)

    period = get_booking_period(period_id=period_id)
    if _is_period_overlaps_another_one(
        housing=period.season.housing, start_date=start_date, end_date=end_date, exclude_ids=[period.id]
    ):
        raise BookingPeriodOverlapping("the new period overlaps at least another existing period.")

    period.start_date = start_date
    period.end_date = end_date
    period.save(update_fields=["start_date", "end_date"])
    return period

def delete_booking_season_period(*, period_id: int) -> None:
    """
    Remove an existing booking period
    """
    period = get_booking_period(period_id=period_id)
    period.delete()
