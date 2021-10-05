from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

from bookings.models import Booking

class BookingAlreadyExists(Exception):
    pass

def book(*, start_date: datetime, end_date: datetime):
    if start_date < timezone.now():
        raise ValidationError("The start date cannot be before today")

    if end_date < start_date:
        raise ValidationError("The end date must be after the start date")

    if Booking.objects.filter(start_date=start_date, end_date=end_date):
        raise BookingAlreadyExists()

    return Booking.objects.create(
        start_date=start_date,
        end_date=end_date,
    )

# give_identity()
# def pay()
# def cancel()
