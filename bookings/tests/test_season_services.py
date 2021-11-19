from datetime import timedelta, date
from unittest.mock import Mock, patch, ANY

from allauth.utils import get_user_model

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from bookings.models.booking import (
    Housing,
    BookingSeason,
    BookingRateModifier,
    BookingPeriod,
    PeriodOfYear,
)
from bookings.exceptions import (
    BookingPeriodOverlapping,
    UnexistingBookingSeason,
    UnexistingBookingRateModifier,
    UnexistingHousing,
    UnexistingBookingPeriod,
)
from bookings.services.season_services import (
    Weekdays,
    create_booking_season,
    update_booking_season,
    delete_booking_season,
    set_season_base_price,
    add_season_rate_modifier,
    update_season_rate_modifier,
    delete_season_rate_modifier,
    add_booking_season_period,
    update_booking_season_period,
    delete_booking_season_period,
)

User = get_user_model()

class BookingSeasonServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Test User')
        self.housing = Housing.objects.create(name="housing 1", user=self.user)
        self.s1 = BookingSeason.objects.create(housing=self.housing, name="s1 - empty season")

        self.start_period = PeriodOfYear(day=1, month=1)
        self.end_period = PeriodOfYear(day=10, month=1)

    # --------------------------------------------------------------
    # SEASONS
    # --------------------------------------------------------------

    def _add_real_seasons_for_tests(self):
        """
        add several seasons with periods:
        s2 : [01/01 - 10/01]
        s3 : [01/02 - 10/02], [20/02 - 04/03]
        """
        self.s2 = BookingSeason.objects.create(housing=self.housing, name="s2 - one period")
        self.s2_p1 = BookingPeriod.objects.create(
            season=self.s2,
            _start_date=PeriodOfYear(day=1, month=1).to_date(),
            _end_date=PeriodOfYear(day=10, month=1).to_date(),
        )
        self.s3 = BookingSeason.objects.create(housing=self.housing, name="s3 - 2 periods")
        self.s3_p1 = BookingPeriod.objects.create(
            season=self.s3,
            _start_date=PeriodOfYear(day=1, month=2).to_date(),
            _end_date=PeriodOfYear(day=10, month=2).to_date(),
        )
        self.s3_p2 = BookingPeriod.objects.create(
            season=self.s3,
            _start_date=PeriodOfYear(day=20, month=2).to_date(),
            _end_date=PeriodOfYear(day=4, month=3).to_date(),
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

    def test_set_base_price_on_unexisting_season(self):
        with self.assertRaises(UnexistingBookingSeason):
            set_season_base_price(season_id=123, base_price=100.0)

    def test_set_base_price_on_existing_season(self):
        set_season_base_price(season_id=self.s1.id, base_price=120.0)
        self.assertEqual(BookingSeason.objects.get(pk=self.s1.id).base_price, 120.0)

    def test_add_rate_modifier_to_an_unexisting_season(self):
        with self.assertRaises(UnexistingBookingSeason):
            add_season_rate_modifier(season_id=123, name="a name", value=1, nb_of_days=1)

    def test_add_rate_modifier_to_an_existing_season_with_default_values(self):
        modifier = add_season_rate_modifier(
            season_id=self.s1.id,
            name="weekends",
            value=20,
            nb_of_days=2,
        )
        self.assertTrue(modifier)
        self.assertEqual(modifier.name, "weekends")
        self.assertEqual(modifier.value, 20)
        self.assertEqual(modifier.minimal_number_of_days, 2)
        self.assertEqual(modifier.is_percent, True)
        self.assertEqual(modifier.is_discount, True)
        self.assertEqual(modifier.monday, True)
        self.assertEqual(modifier.tuesday, True)
        self.assertEqual(modifier.wednesday, True)
        self.assertEqual(modifier.thursday, True)
        self.assertEqual(modifier.friday, True)
        self.assertEqual(modifier.saturday, True)
        self.assertEqual(modifier.sunday, True)

    def test_add_rate_modifier_to_an_existing_season_without_default_values(self):
        modifier = add_season_rate_modifier(
            season_id=self.s1.id,
            name="weekends",
            value=20,
            nb_of_days=2,
            is_percent=True,
            is_discount=False,
            weekdays=Weekdays(mon=False, tue=False, wed=False, thu=False, fri=False, sat=True, sun=True)
        )
        self.assertTrue(modifier)
        self.assertEqual(modifier.name, "weekends")
        self.assertEqual(modifier.value, 20)
        self.assertEqual(modifier.minimal_number_of_days, 2)
        self.assertEqual(modifier.is_percent, True)
        self.assertEqual(modifier.is_discount, False)
        self.assertEqual(modifier.monday, False)
        self.assertEqual(modifier.tuesday, False)
        self.assertEqual(modifier.wednesday, False)
        self.assertEqual(modifier.thursday, False)
        self.assertEqual(modifier.friday, False)
        self.assertEqual(modifier.saturday, True)
        self.assertEqual(modifier.sunday, True)

    def test_update_an_unexisting_rate_modifier(self):
        with self.assertRaises(UnexistingBookingRateModifier):
            update_season_rate_modifier(
                modifier_id=123,
                name="no name",
                value=1,
                nb_of_days=1,
                is_percent=False,
                is_discount=False,
                weekdays=Weekdays(mon=False, tue=False, wed=False, thu=False, fri=False, sat=True, sun=True)
            )

    def test_update_an_existing_rate_modifier(self):
        modifier = BookingRateModifier.objects.create(
            season=self.s1,
            name="weekends",
            value=1,
            minimal_number_of_days=2
        )
        updated_modifier = update_season_rate_modifier(
            modifier_id=modifier.id,
            name="week",
            value=30,
            nb_of_days=7,
            is_percent=False,
            is_discount=False,
            weekdays=Weekdays()
        )
        self.assertTrue(updated_modifier)
        self.assertEqual(updated_modifier.id, modifier.id)
        self.assertEqual(updated_modifier.name, "week")
        self.assertEqual(updated_modifier.value, 30)
        self.assertEqual(updated_modifier.minimal_number_of_days, 7)
        self.assertEqual(updated_modifier.is_percent, False)
        self.assertEqual(updated_modifier.is_discount, False)
        self.assertEqual(updated_modifier.monday, True)
        self.assertEqual(updated_modifier.tuesday, True)
        self.assertEqual(updated_modifier.wednesday, True)
        self.assertEqual(updated_modifier.thursday, True)
        self.assertEqual(updated_modifier.friday, True)
        self.assertEqual(updated_modifier.saturday, True)
        self.assertEqual(updated_modifier.sunday, True)

    def test_delete_an_unexisting_rate_modifier(self):
        with self.assertRaises(UnexistingBookingRateModifier):
            delete_season_rate_modifier(modifier_id=123)

    def test_delete_an_existing_rate_modifier(self):
        modifier = BookingRateModifier.objects.create(
            season=self.s1,
            name="weekends",
            value=1,
            minimal_number_of_days=2
        )
        delete_season_rate_modifier(modifier_id=modifier.id)
        self.assertFalse(BookingRateModifier.objects.filter(pk=modifier.id))

    # --------------------------------------------------------------
    # PERIODS
    # --------------------------------------------------------------

    def test_add_period_to_unexisting_season(self):
        with self.assertRaises(UnexistingBookingSeason):
            add_booking_season_period(
                season_id=123,
                start_period=self.start_period,
                end_period=self.end_period,
            )

    def test_add_period_to_season(self):
        period = add_booking_season_period(
            season_id=self.s1.id, start_period=self.start_period, end_period=self.end_period
        )
        self.assertEqual(period.season, self.s1)
        self.assertEqual(period.start_period, self.start_period)
        self.assertEqual(period.end_period, self.end_period)

    def test_add_period_to_season_with_overlap_inside_the_season(self):
        self._add_real_seasons_for_tests()

        with self.assertRaises(BookingPeriodOverlapping):
            add_booking_season_period(
                season_id=self.s2.id,
                start_period=self.s2_p1.end_period,  # the second period overlaps the first period
                end_period=self.s2_p1.end_period + 5
            )

    def test_add_period_to_season_with_overlap_inside_another_season(self):
        self._add_real_seasons_for_tests()

        with self.assertRaises(BookingPeriodOverlapping):
            add_booking_season_period(
                season_id=self.s2.id,
                start_period=self.s3_p2.end_period,  # the second period overlaps the first period
                end_period=self.s3_p2.end_period + 5
            )

    @patch("bookings.services.season_services.PeriodOfYear.check_range", Mock(side_effect=ValidationError("error")))
    def test_add_period_raise_error_if_invalid_dates(self):
        with self.assertRaises(ValidationError):
            add_booking_season_period(
                season_id=self.s1.id,
                start_period=self.start_period,
                end_period=self.end_period,
            )

    def test_update_unexisting_period(self):
        with self.assertRaises(UnexistingBookingPeriod):
            update_booking_season_period(
                period_id=123,
                start_period=self.start_period,
                end_period=self.end_period
            )

    def test_update_an_existing_period(self):
        self._add_real_seasons_for_tests()

        new_start_period = self.s2_p1.start_period + 1
        new_end_period = self.s2_p1.end_period + 2

        period = update_booking_season_period(
            period_id=self.s2_p1.id, start_period=new_start_period, end_period=new_end_period,
        )

        self.assertEqual(period.id, self.s2_p1.id)
        self.assertEqual(period.start_period, new_start_period)
        self.assertEqual(period.end_period, new_end_period)

    def test_update_an_existing_period_with_overlap(self):
        self._add_real_seasons_for_tests()

        new_start_period = self.s3_p1.end_period
        new_end_period = new_start_period + 2

        with self.assertRaises(BookingPeriodOverlapping):
            update_booking_season_period(
                period_id=self.s2_p1.id, start_period=new_start_period, end_period=new_end_period,
            )

    @patch("bookings.services.season_services.PeriodOfYear.check_range", Mock(side_effect=ValidationError("error")))
    def test_update_period_raise_error_if_invalid_dates(self):
        self._add_real_seasons_for_tests()

        with self.assertRaises(ValidationError):
            update_booking_season_period(
                period_id=self.s2_p1.id,
                start_period=self.start_period,
                end_period=self.end_period,
            )

    def test_delete_an_unexisting_period(self):
        with self.assertRaises(UnexistingBookingPeriod):
            delete_booking_season_period(period_id=123)

    def test_delete_an_existing_period(self):
        self._add_real_seasons_for_tests()

        delete_booking_season_period(period_id=self.s2_p1.id)
        self.assertFalse(BookingPeriod.objects.filter(pk=self.s2_p1.id))
