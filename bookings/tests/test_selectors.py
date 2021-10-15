from datetime import date
from django.test import TestCase
# from django.core.exceptions import ValidationError
# from django.utils import timezone

# from bookings import services
# from bookings.models import Booking

# from bookings.models import (
#     Housing,
#     BookingSeason,
#     BookingPeriod,
#     BookingRateModifier,
#     PeriodOfYear,
# )
from bookings.models import (
    Housing,
    BookingSeason,
    PeriodOfYear,
    BookingDate,
    BookingDateSet,
)
from bookings.services import (
    add_booking_season_period,
)
from bookings.exceptions import (
    BookingSeasonNoMatchFound,
)
from bookings.selectors import (
    explode_booking_dates_in_season_periods,
)

class SelectorTests(TestCase):

    def setUp(self):
        self.maxDiff = None

        self.housing = Housing.objects.create(name="housing 1")
        self.low_season = BookingSeason.objects.create(housing=self.housing, name="low season", base_price=80)
        self.med_season = BookingSeason.objects.create(housing=self.housing, name="medium season", base_price=90)
        self.high_season = BookingSeason.objects.create(housing=self.housing, name="high season", base_price=100)

        # create 3 seasons:
        # - low    : [15/01 - 31/03] + [01/11 - 31/12]
        # - medium : [01/04 - 31/05] + [01/09 - 31/10]
        # - high   : [01/06 - 31/08]
        self.low_season_p1 = add_booking_season_period(
            season_id=self.low_season.id,
            start_period=PeriodOfYear(15, 1),
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

    def test_explode_booking_dates_didnt_find_any_season(self):
        seasons = explode_booking_dates_in_season_periods(
            housing=self.housing,
            booking_date=BookingDate(
                start=date(day=1, month=1, year=2021),
                end=date(day=10, month=1, year=2021)
            ),
        )
        self.assertDictEqual(seasons, {})

    def test_explode_booking_dates_returns_one_period_for_one_season(self):
        booking_date = BookingDate(
            start=date(day=15, month=1, year=2021),
            end=date(day=10, month=3, year=2021),
        )
        seasons = explode_booking_dates_in_season_periods(housing=self.housing, booking_date=booking_date)

        expected_result = {
            self.low_season.id: BookingDateSet(season=self.low_season, nb_of_nights=54, dates=(booking_date,)),
        }
        self.assertEqual(seasons, expected_result)

    def test_explode_booking_dates_returns_2_periods_for_2_seasons(self):
        booking_date = BookingDate(
            start=date(day=20, month=1, year=2021),
            end=date(day=15, month=4, year=2021),
        )
        seasons = explode_booking_dates_in_season_periods(housing=self.housing, booking_date=booking_date)

        expected_low_season_dates = (
            BookingDate(start=date(day=20, month=1, year=2021), end=date(day=31, month=3, year=2021),),
        )
        expected_med_season_dates = (
            BookingDate(start=date(day=1, month=4, year=2021), end=date(day=15, month=4, year=2021),),
        )
        expected_result = {
            self.low_season.id: BookingDateSet(season=self.low_season, nb_of_nights=71, dates=expected_low_season_dates),
            self.med_season.id: BookingDateSet(season=self.med_season, nb_of_nights=14, dates=expected_med_season_dates),
        }
        self.assertDictEqual(seasons, expected_result)

    def test_explode_booking_dates_returns_several_periods_for_2_seasons(self):
        booking_date = BookingDate(
            start=date(day=15, month=4, year=2021),
            end=date(day=15, month=9, year=2021),
        )
        seasons = explode_booking_dates_in_season_periods(housing=self.housing, booking_date=booking_date)

        expected_med_season_dates = (
            BookingDate(start=date(day=15, month=4, year=2021), end=date(day=31, month=5, year=2021),),
            BookingDate(start=date(day=1, month=9, year=2021), end=date(day=15, month=9, year=2021),),
        )
        expected_high_season_dates = (
            BookingDate(start=date(day=1, month=6, year=2021), end=date(day=31, month=8, year=2021),),
        )
        expected_result = {
            self.med_season.id: BookingDateSet(season=self.med_season, nb_of_nights=61, dates=expected_med_season_dates),
            self.high_season.id: BookingDateSet(season=self.high_season, nb_of_nights=92, dates=expected_high_season_dates),
        }
        self.assertDictEqual(seasons, expected_result)

    def test_explode_booking_dates_returns_all_periods_of_the_year(self):
        booking_date = BookingDate(
            start=date(day=15, month=1, year=2021),
            end=date(day=31, month=12, year=2021),
        )
        seasons = explode_booking_dates_in_season_periods(housing=self.housing, booking_date=booking_date)

        expected_low_season_dates = (
            BookingDate(start=date(day=15, month=1, year=2021), end=date(day=31, month=3, year=2021),),
            BookingDate(start=date(day=1, month=11, year=2021), end=date(day=31, month=12, year=2021),),
        )
        expected_med_season_dates = (
            BookingDate(start=date(day=1, month=4, year=2021), end=date(day=31, month=5, year=2021),),
            BookingDate(start=date(day=1, month=9, year=2021), end=date(day=31, month=10, year=2021),),
        )
        expected_high_season_dates = (
            BookingDate(start=date(day=1, month=6, year=2021), end=date(day=31, month=8, year=2021),),
        )
        expected_result = {
            self.low_season.id: BookingDateSet(season=self.low_season, nb_of_nights=136, dates=expected_low_season_dates),
            self.med_season.id: BookingDateSet(season=self.med_season, nb_of_nights=122, dates=expected_med_season_dates),
            self.high_season.id: BookingDateSet(season=self.high_season, nb_of_nights=92, dates=expected_high_season_dates),
        }
        self.assertDictEqual(seasons, expected_result)
