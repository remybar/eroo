from collections import namedtuple
from collections.abc import Sequence
from datetime import date
from typing import Union

from django.core.exceptions import ValidationError
from django.utils import timezone

from bookings.models import BookingDate

Range = namedtuple("Range", ["start", "end"])

def _intersect_two_ranges(range1: Range, range2: Range) -> Union[Range, None]:
    new_range = Range(
        max(range1.start, range2.start),
        min(range1.end, range2.end)
    )
    return new_range if new_range.start <= new_range.end else None

def _intersect_all(input_range: Range, ranges: Sequence[Range]) -> bool:
    return any(
        _intersect_two_ranges(input_range, r)
        for r in ranges
    )

def _check_dates(booking_date: BookingDate):
    """
    Check start/end dates consistency.
    """
    if booking_date.start < timezone.now().date():
        raise ValidationError("The start date cannot be before today")

    if booking_date.end < booking_date.start:
        raise ValidationError("The end date must be after the start date")
