class BookingAlreadyExists(Exception):
    pass

class UnexistingHousing(Exception):
    pass

class UnexistingBookingSeason(Exception):
    pass

class UnexistingBookingPeriod(Exception):
    pass

class BookingPeriodOverlapping(Exception):
    pass
