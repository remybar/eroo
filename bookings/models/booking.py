from django.db import models

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

    def __str__(self):
        return self.name

class BookingPeriod(models.Model):
    """
    Period of time used to define a season
    """
    season = models.ForeignKey(BookingSeason, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "f{self.start_date.strftime('%d-%m-%Y')} - {self.end_date.strftime('%d-%m-%Y')}"

class BookingPriceCategory(models.Model):
    """
    A price category such as 'adult', 'child', 'baby'.
    """
    housing = models.ForeignKey(Housing, on_delete=models.CASCADE)

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)

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
