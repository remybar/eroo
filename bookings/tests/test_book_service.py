from datetime import datetime, timedelta
from unittest.mock import Mock, patch, ANY

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from bookings import services
from bookings.models import Booking

from bookings.exceptions import (
    BookingSeasonNoMatchFound,
)
from bookings.models import (
    Housing,
    BookingSeason,
    BookingPeriod,
    BookingRateModifier,
    PeriodOfYear,
)
from bookings.services.season_services import (
    create_booking_season,
    add_booking_season_period,
)
from bookings.services.booking_services import (
    compute_price,
)

class BookServiceTests(TestCase):

    def setUp(self):
        self.start_period = PeriodOfYear(day=1, month=1)
        self.end_period = PeriodOfYear(day=10, month=1)

    def _create_data_for_test(self):
        self.housing = Housing.objects.create(name="housing 1")
        self.low_season = BookingSeason.objects.create(housing=self.housing, name="low season", base_price=80)
        self.med_season = BookingSeason.objects.create(housing=self.housing, name="medium season", base_price=90)
        self.high_season = BookingSeason.objects.create(housing=self.housing, name="high season", base_price=100)

        # create 3 seasons:
        # - low    : [01/01 - 31/03] + [01/11 - 31/12]
        # - medium : [01/04 - 31/05] + [01/09 - 31/10]
        # - high   : [01/06 - 31/08]
        self.low_season_p1 = add_booking_season_period(
            season_id=self.low_season_p1.id,
            start_period=PeriodOfYear(1, 1),
            end_period=PeriodOfYear(31, 3)
        )
        self.low_season_p2 = add_booking_season_period(
            season_id=self.low_season_p1.id,
            start_period=PeriodOfYear(1, 11),
            end_period=PeriodOfYear(31, 12)
        )
        self.med_season_p1 = add_booking_season_period(
            season_id=self.low_season_p1.id,
            start_period=PeriodOfYear(1, 4),
            end_period=PeriodOfYear(31, 5)
        )
        self.med_season_p2 = add_booking_season_period(
            season_id=self.low_season_p1.id,
            start_period=PeriodOfYear(1, 9),
            end_period=PeriodOfYear(31, 10)
        )
        self.high_season_p1 = add_booking_season_period(
            season_id=self.low_season_p1.id,
            start_period=PeriodOfYear(1, 6),
            end_period=PeriodOfYear(31, 8)
        )

    # def test_compute_price_for_an_undefined_period(self):
    #     with self.assertRaises(BookingSeasonNoMatchFound):
    #         price = compute_price(start_date=self.start_date, end_date=self.end_date)

    # @patch("bookings.services.booking_services._check_dates", Mock(side_effect=ValidationError("error")))
    # def test_compute_price_with_invalid_dates(self):
    #     with self.assertRaises(ValidationError):
    #         price = compute_price(start_date=self.start_date, end_date=self.end_date)

    # def test_compute_price_for_one_night_without_any_rate_modifiers(self):
    #     self._create_data_for_test()

    #     price = compute_price(
    #         start_date=self.low_season_p1.start_date,
    #         end_date=self.low_season_p1.start_date + timedelta(days=1)
    #     )

    #     self.assertEqual(price, self.low_season.base_price)








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
