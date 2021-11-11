from collections import namedtuple
from datetime import date, timedelta
from typing import TypeVar

from django.db import models
from django.core.exceptions import ValidationError

Weekdays = namedtuple('Weekdays', ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'], defaults=7 * [True])

DEFAULT_YEAR = 2021

BookingDate = namedtuple('BookingDate', ['start', 'end'])
BookingDateSet = namedtuple('BookingDateSet', ['season', 'nb_of_nights', 'dates'])

T = TypeVar('T', bound='PeriodOfYear')
class PeriodOfYear(namedtuple('PeriodOfYear', ['day', 'month'])):

    def __str__(self):
        return f"{self.day}/{self.month}"

    def from_date(d: date):
        return PeriodOfYear(day=d.day, month=d.month)

    def to_date(self) -> date:
        return date(day=self.day, month=self.month, year=DEFAULT_YEAR)

    def __eq__(self, other):
        return self.day == other.day and self.month == other.month

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.month < other.month or (self.month == other.month and self.day < other.day)

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return self > other or self == other

    def __add__(self, days: int) -> T:
        return PeriodOfYear.from_date(self.to_date() + timedelta(days=days))

    def __sub__(self, days: int) -> T:
        return PeriodOfYear.from_date(self.to_date() - timedelta(days=days))

    def check_range(start_period: T, end_period: T):
        """
        Check start/end period consistency.
        A period in defined with a day and a month. The year is not used.
        """
        if end_period < start_period:
            raise ValidationError("The end period must be after the start period")

class Housing(models.Model):
    """
    A housing to rent.
    """
    name = models.CharField(max_length=256)

class BookingSeason(models.Model):
    """
    Set of periods of time to define a list of homogeneous rates.
    Ex: low season from january to march and october to december.
    """
    housing = models.ForeignKey(Housing, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    base_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

class BookingPeriod(models.Model):
    """
    Period of time used to define a season
    """
    season = models.ForeignKey(BookingSeason, on_delete=models.CASCADE, related_name="periods")

    _start_date = models.DateField()
    _end_date = models.DateField()

    def __str__(self):
        start = self._start_date.strftime("%d/%m")
        end = self._end_date.strftime("%d/%m")
        return f"{start} - {end}"

    @property
    def name(self) -> str:
        return f"{str(self.start_period)} - {str(self.end_period)}"

    @property
    def start_period(self) -> PeriodOfYear:
        return PeriodOfYear.from_date(self._start_date)

    @start_period.setter
    def start_period(self, period: PeriodOfYear) -> None:
        self._start_date = period.to_date()

    @property
    def end_period(self) -> PeriodOfYear:
        return PeriodOfYear.from_date(self._end_date)

    @end_period.setter
    def end_period(self, period: PeriodOfYear) -> None:
        self._end_date = period.to_date()

class BookingRateModifier(models.Model):
    """
    Discount/Increase of booking rate applied on season base price, according to some conditions.
    Example: +20% on weekends (2 days in [saturday, sunday]).
    """
    season = models.ForeignKey(BookingSeason, on_delete=models.CASCADE)

    name = models.CharField(max_length=32)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    is_percent = models.BooleanField(default=True)
    is_discount = models.BooleanField(default=True)
    minimal_number_of_days = models.IntegerField()
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)

    @property
    def weekdays(self) -> Weekdays:
        return Weekdays(
            mon=self.monday,
            tue=self.tuesday,
            wed=self.wednesday,
            thu=self.thursday,
            fri=self.friday,
            sat=self.saturday,
            sun=self.sunday,
        )

    @weekdays.setter
    def weekdays(self, weekdays: Weekdays) -> None:
        self.monday = weekdays.mon
        self.tuesday = weekdays.tue
        self.wednesday = weekdays.wed
        self.thursday = weekdays.thu
        self.friday = weekdays.fri
        self.saturday = weekdays.sat
        self.sunday = weekdays.sun

class BookingPriceCategory(models.Model):
    """
    A price category such as 'adult', 'child', 'baby'.
    """
    housing = models.ForeignKey(Housing, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class BookingPrice(models.Model):
    """
    A price depending of the guest category (adult, child, baby...)
    """
    category = models.ForeignKey(BookingPriceCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)

class BookingRate(models.Model):
    """
    Rate for one or more specific season(s) and one or more specific period(s).
    Ex: 100€/night for low and mid season, for a single day or in a midweek.
    """
    seasons = models.ManyToManyField(BookingSeason)
    periods = models.ManyToManyField(BookingPeriod)

    # 'per night' prices
    base_price = models.DecimalField(max_digits=7, decimal_places=2)
    extra_guest_price = models.ManyToManyField(BookingPrice)

class BookingFee(models.Model):
    """
    Additional fees
    """
    seasons = models.ManyToManyField(BookingSeason)
    periods = models.ManyToManyField(BookingPeriod)

    name = models.CharField(max_length=128)
    guest_price = models.ManyToManyField(BookingPrice)
    is_per_night = models.BooleanField()
    is_per_guest = models.BooleanField()
    # TODO: possibilité d'ajouter une qté par exemple 3 bouteilles de vin / jour (ou / séjour)

class Booking(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    housing = models.ForeignKey(Housing, on_delete=models.CASCADE)


# TODO: ajouter les taxes
# TODO: ajouter les discounts ? (ou déjà géré via season/period) ?
