from datetime import timedelta, date
from unittest.mock import Mock, patch, ANY

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from bookings.models.booking import Housing, BookingSeason, BookingPeriod
from bookings.exceptions import (
    BookingPeriodOverlapping,
    UnexistingBookingSeason,
    UnexistingHousing,
    UnexistingBookingPeriod,
)
from bookings.services.season_services import (
    create_booking_season,
    update_booking_season,
    delete_booking_season,
    add_booking_season_period,
    update_booking_season_period,
    delete_booking_season_period,
)

def _today(plus: int = None, minus: int = None) -> date:
    d = timezone.now().date()
    if plus:
        d += timedelta(days=plus)
    if minus:
        d -= timedelta(days=minus)
    return d

class BookingSeasonServiceTests(TestCase):

    def setUp(self):
        self.housing = Housing.objects.create(name="housing 1")
        self.s1 = BookingSeason.objects.create(housing=self.housing, name="s1 - empty season")

    def _add_real_seasons_for_tests(self):
        """
        add several seasons with periods:
        s2 : [today() - today() + 10]
        s3 : [today() + 20 - today() + 30], [today() + 40 - today() + 50]
        """
        self.s2 = BookingSeason.objects.create(housing=self.housing, name="s2 - one period")
        self.s2_p1 = BookingPeriod.objects.create(
            season=self.s2, start_date=_today(), end_date=_today(plus=10)
        )
        self.s3 = BookingSeason.objects.create(housing=self.housing, name="s3 - 2 periods")
        self.s3_p1 = BookingPeriod.objects.create(
            season=self.s3, start_date=_today(plus=20), end_date=_today(plus=30)
        )
        self.s3_p2 = BookingPeriod.objects.create(
            season=self.s3, start_date=_today(plus=30), end_date=_today(plus=40)
        )

    def test_create_a_new_booking_season(self):
        season = create_booking_season(housing=self.housing, name="season name")
        self.assertEqual(season.name, "season name")

    def test_update_a_unexisting_booking_season(self):
        with self.assertRaises(UnexistingBookingSeason):
            update_booking_season(season_id=123, new_name="new name")

    def test_update_a_booking_season(self):
        updated_season = update_booking_season(season_id=self.s1.id, new_name="new name")
        self.assertEqual(updated_season.id, self.s1.id)
        self.assertEqual(updated_season.name, "new name")

    def test_delete_a_unexisting_booking_season(self):
        with self.assertRaises(UnexistingBookingSeason):
            delete_booking_season(season_id=123)

    def test_delete_a_booking_season(self):
        delete_booking_season(season_id=self.s1.id)
        self.assertFalse(BookingSeason.objects.filter(pk=self.s1.id))

    def test_add_period_to_unexisting_season(self):
        with self.assertRaises(UnexistingBookingSeason):
            add_booking_season_period(season_id=123, start_date=_today(), end_date=_today(plus=10))

    def test_add_period_to_season(self):
        start_date = _today()
        end_date = _today(plus=10)

        period = add_booking_season_period(season_id=self.s1.id, start_date=start_date, end_date=end_date)
        self.assertEqual(period.season, self.s1)
        self.assertEqual(period.start_date, start_date)
        self.assertEqual(period.end_date, end_date)

    def test_add_period_to_season_with_overlap_inside_the_season(self):
        self._add_real_seasons_for_tests()

        with self.assertRaises(BookingPeriodOverlapping):
            add_booking_season_period(
                season_id=self.s2.id,
                start_date=self.s2_p1.end_date,  # the second period overlaps the first period
                end_date=self.s2_p1.end_date + timedelta(days=5)
            )

    def test_add_period_to_season_with_overlap_inside_another_season(self):
        self._add_real_seasons_for_tests()

        with self.assertRaises(BookingPeriodOverlapping):
            add_booking_season_period(
                season_id=self.s2.id,
                start_date=self.s3_p2.end_date,  # the second period overlaps the first period
                end_date=self.s3_p2.end_date + timedelta(days=5)
            )

    @patch("bookings.services.season_services._check_dates", Mock(side_effect=ValidationError("error")))
    def test_add_period_raise_error_if_invalid_dates(self):
        with self.assertRaises(ValidationError):
            add_booking_season_period(season_id=self.s1.id, start_date=_today(), end_date=_today(plus=1))

    def test_update_unexisting_period(self):
        with self.assertRaises(UnexistingBookingPeriod):
            update_booking_season_period(period_id=123, start_date=_today(), end_date=_today(plus=10))

    def test_update_an_existing_period(self):
        self._add_real_seasons_for_tests()

        new_start_date = self.s2_p1.start_date + timedelta(days=1)
        new_end_date = self.s2_p1.end_date + timedelta(days=2)

        period = update_booking_season_period(
            period_id=self.s2_p1.id, start_date=new_start_date, end_date=new_end_date,
        )

        self.assertEqual(period.id, self.s2_p1.id)
        self.assertEqual(period.start_date, new_start_date)
        self.assertEqual(period.end_date, new_end_date)

    def test_update_an_existing_period_with_overlap(self):
        self._add_real_seasons_for_tests()

        new_start_date = self.s3_p1.end_date
        new_end_date = new_start_date + timedelta(days=2)

        with self.assertRaises(BookingPeriodOverlapping):
            update_booking_season_period(
                period_id=self.s2_p1.id, start_date=new_start_date, end_date=new_end_date,
            )

    @patch("bookings.services.season_services._check_dates", Mock(side_effect=ValidationError("error")))
    def test_update_period_raise_error_if_invalid_dates(self):
        self._add_real_seasons_for_tests()

        with self.assertRaises(ValidationError):
            update_booking_season_period(
                period_id=self.s2_p1.id, start_date=_today(), end_date=_today(plus=1),
            )

    def test_delete_an_unexisting_period(self):
        with self.assertRaises(UnexistingBookingPeriod):
            delete_booking_season_period(period_id=123)

    def test_delete_an_existing_period(self):
        self._add_real_seasons_for_tests()

        delete_booking_season_period(period_id=self.s2_p1.id)
        self.assertFalse(BookingPeriod.objects.filter(pk=self.s2_p1.id))
