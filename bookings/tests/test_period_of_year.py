from django.test import TestCase

from bookings.models import (
    PeriodOfYear,
)

class PeriodOfYearTests(TestCase):

    def test_eq_operator(self):
        self.assertNotEqual(PeriodOfYear(day=5, month=2), PeriodOfYear(day=1, month=3))
        self.assertNotEqual(PeriodOfYear(day=1, month=2), PeriodOfYear(day=1, month=3))
        self.assertNotEqual(PeriodOfYear(day=2, month=3), PeriodOfYear(day=1, month=3))
        self.assertEqual(PeriodOfYear(day=4, month=2), PeriodOfYear(day=4, month=2))

    def test_lt_operator(self):
        self.assertTrue(PeriodOfYear(day=12, month=2) < PeriodOfYear(day=1, month=3))
        self.assertTrue(PeriodOfYear(day=1, month=2) < PeriodOfYear(day=2, month=2))
        self.assertFalse(PeriodOfYear(day=1, month=3) < PeriodOfYear(day=1, month=2))
        self.assertFalse(PeriodOfYear(day=2, month=2) < PeriodOfYear(day=1, month=2))

    def test_le_operator(self):
        self.assertTrue(PeriodOfYear(day=12, month=2) <= PeriodOfYear(day=1, month=3))
        self.assertTrue(PeriodOfYear(day=1, month=2) <= PeriodOfYear(day=2, month=2))
        self.assertFalse(PeriodOfYear(day=1, month=3) <= PeriodOfYear(day=1, month=2))
        self.assertFalse(PeriodOfYear(day=2, month=2) <= PeriodOfYear(day=1, month=2))
        self.assertTrue(PeriodOfYear(day=2, month=2) <= PeriodOfYear(day=2, month=2))
