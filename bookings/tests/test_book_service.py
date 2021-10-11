from datetime import datetime, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from bookings import services
from bookings.models import Booking

class BookServiceTests(TestCase):

    def setUp(self):
        self.start_date = timezone.now() + timedelta(days=1)
        self.end_date = timezone.now() + timedelta(days=2)

    # def test_booking_creates_a_new_booking_object(self):

    #     booking = services.book(start_date=self.start_date, end_date=self.end_date)

    #     self.assertTrue(booking.id)
    #     self.assertEqual(booking.start_date, self.start_date)
    #     self.assertEqual(booking.end_date, self.end_date)

    # def test_book_raise_error_if_start_date_not_in_the_future(self):
    #     start_date = timezone.now() - timedelta(days=1)

    #     with self.assertRaises(ValidationError) as error:
    #         booking = services.book(start_date=start_date, end_date=self.end_date)

    # def test_book_raise_error_if_end_date_is_before_start_date(self):
    #     with self.assertRaises(ValidationError) as error:
    #         booking = services.book(start_date=self.end_date, end_date=self.start_date)

    # def test_book_raise_error_if_a_booking_already_exists(self):
    #     Booking.objects.create(start_date=self.start_date, end_date=self.end_date)

    #     with self.assertRaises(services.BookingAlreadyExists) as error:
    #         booking = services.book(start_date=self.start_date, end_date=self.end_date)
