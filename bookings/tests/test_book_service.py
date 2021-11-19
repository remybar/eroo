from datetime import date, datetime, timedelta
from unittest.mock import Mock, patch, ANY

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from allauth.utils import get_user_model

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
    BookingDate,
)
from bookings.services.season_services import (
    create_booking_season,
    add_booking_season_period,
)
from bookings.services.booking_services import (
    compute_price,
)

User = get_user_model()

class BookServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Test User')
        self.housing = Housing.objects.create(name="housing 1", user=self.user)
        self.booking_date = BookingDate(
            start=date(day=1, month=1, year=2021),
            end=date(day=10, month=1, year=2021),
        )

    def _create_data_for_test(self):
        self.low_season = BookingSeason.objects.create(housing=self.housing, name="low season", base_price=80)
        self.med_season = BookingSeason.objects.create(housing=self.housing, name="medium season", base_price=90)
        self.high_season = BookingSeason.objects.create(housing=self.housing, name="high season", base_price=100)

        # create 3 seasons:
        # - low    : [01/01 - 31/03] + [01/11 - 31/12]
        # - medium : [01/04 - 31/05] + [01/09 - 31/10]
        # - high   : [01/06 - 31/08]
        self.low_season_p1 = add_booking_season_period(
            season_id=self.low_season.id,
            start_period=PeriodOfYear(1, 1),
            end_period=PeriodOfYear(31, 3)
        )
        self.low_season_p2 = add_booking_season_period(
            season_id=self.low_season.id,
            start_period=PeriodOfYear(1, 11),
            end_period=PeriodOfYear(31, 12)
        )
        self.med_season_p1 = add_booking_season_period(
            season_id=self.med_season.id,
            start_period=PeriodOfYear(1, 4),
            end_period=PeriodOfYear(31, 5)
        )
        self.med_season_p2 = add_booking_season_period(
            season_id=self.med_season.id,
            start_period=PeriodOfYear(1, 9),
            end_period=PeriodOfYear(31, 10)
        )
        self.high_season_p1 = add_booking_season_period(
            season_id=self.high_season.id,
            start_period=PeriodOfYear(1, 6),
            end_period=PeriodOfYear(31, 8)
        )

    def _create_rate_modifiers_for_tests(self):
        pass

    @patch("bookings.services.booking_services._check_dates", Mock(side_effect=ValidationError("error")))
    def test_compute_price_with_invalid_dates(self):
        with self.assertRaises(ValidationError):
            price = compute_price(housing=self.housing, booking_date=self.booking_date)

    @patch("bookings.services.booking_services._check_dates", Mock())
    def test_compute_price_for_an_undefined_period(self):
        with self.assertRaises(BookingSeasonNoMatchFound):
            price = compute_price(housing=self.housing, booking_date=self.booking_date)

    @patch("bookings.services.booking_services._check_dates", Mock())
    def test_compute_price_for_one_night(self):
        self._create_data_for_test()

        price = compute_price(
            housing=self.housing,
            booking_date=BookingDate(
                start=self.low_season_p1.start_period.to_date(),
                end=self.low_season_p1.start_period.to_date() + timedelta(days=1),
            )
        )
        self.assertEqual(price, self.low_season.base_price)

    @patch("bookings.services.booking_services._check_dates", Mock())
    def test_compute_price_for_three_nights_same_season(self):
        self._create_data_for_test()

        price = compute_price(
            housing=self.housing,
            booking_date=BookingDate(
                start=self.low_season_p1.start_period.to_date(),
                end=self.low_season_p1.start_period.to_date() + timedelta(days=3),
            )
        )
        self.assertEqual(price, self.low_season.base_price * 3)

    @patch("bookings.services.booking_services._check_dates", Mock())
    def test_compute_price_for_five_nights_two_seasons(self):
        self._create_data_for_test()

        price = compute_price(
            housing=self.housing,
            booking_date=BookingDate(
                start=self.med_season_p1.end_period.to_date() - timedelta(days=2),
                end=self.high_season_p1.start_period.to_date() + timedelta(days=2),
            )
        )
        self.assertEqual(price, self.med_season.base_price * 3 + self.high_season.base_price * 2)

    @patch("bookings.services.booking_services._check_dates", Mock())
    def test_compute_price_for_all_the_year(self):
        self._create_data_for_test()

        price = compute_price(
            housing=self.housing,
            booking_date=BookingDate(
                start=self.low_season_p1.start_period.to_date(),
                end=self.low_season_p2.end_period.to_date(),
            )
        )
        self.assertEqual(
            price,
            (
                self.low_season.base_price * (
                    (self.low_season_p1._end_date - self.low_season_p1._start_date).days + 1 +
                    (self.low_season_p2._end_date - self.low_season_p2._start_date).days
                ) +
                self.med_season.base_price * (
                    (self.med_season_p1._end_date - self.med_season_p1._start_date).days + 1 +
                    (self.med_season_p2._end_date - self.med_season_p2._start_date).days + 1
                ) +
                self.high_season.base_price * (
                    (self.high_season_p1._end_date - self.high_season_p1._start_date).days + 1
                )
            )
        )

    def test_compute_price_for_one_night_with_one_rate_modifier(self):
        pass

    def test_compute_price_for_one_night_with_several_rate_modifiers(self):
        pass

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
