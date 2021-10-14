class BookingAlreadyExists(Exception):
    pass

class UnexistingHousing(Exception):
    pass

class UnexistingBookingSeason(Exception):
    pass

class UnexistingBookingRateModifier(Exception):
    pass

class UnexistingBookingPeriod(Exception):
    pass

class UnexistingBookingPriceCategory(Exception):
    pass

class BookingPeriodOverlapping(Exception):
    pass

class BookingSeasonNoMatchFound(Exception):
    pass
