from datetime import datetime, timedelta
from unittest.mock import Mock, patch, ANY

from django.test import TestCase

from bookings.utils import _intersect_two_ranges, Range, _intersect_all

class UtilTests(TestCase):

    def test_a_range_is_on_the_left(self):
        """
                    |----|
            |---|
        """
        s1 = 5
        e1 = 10
        s2 = 1
        e2 = 4

        self.assertFalse(
            _intersect_two_ranges(
                Range(start=s1, end=e1),
                Range(start=s2, end=e2),
            )
        )

    def test_intersect_range_on_the_left(self):
        """
               |------------|
            |--|
        """
        s1 = 5
        e1 = 10
        s2 = 3
        e2 = s1

        self.assertTrue(
            _intersect_two_ranges(
                Range(start=s1, end=e1),
                Range(start=s2, end=e2),
            )
        )

    def test_a_range_is_on_the_right(self):
        """
            |---|
                    |----|
        """
        s1 = 1
        e1 = 4
        s2 = 6
        e2 = 10

        self.assertFalse(
            _intersect_two_ranges(
                Range(start=s1, end=e1),
                Range(start=s2, end=e2),
            )
        )

    def test_intersect_range_on_the_right(self):
        """
           |------------|
                        |------|
        """
        s1 = 1
        e1 = 5
        s2 = e1
        e2 = 10

        self.assertTrue(
            _intersect_two_ranges(
                Range(start=s1, end=e1),
                Range(start=s2, end=e2),
            )
        )

    def test_a_range_includes_the_other(self):
        """
            |------------|
                |----|
        """
        s1 = 1
        e1 = 10
        s2 = 3
        e2 = 5

        self.assertTrue(
            _intersect_two_ranges(
                Range(start=s1, end=e1),
                Range(start=s2, end=e2),
            )
        )

    def test_a_range_is_included_in_the_other(self):
        """
                |----|
            |------------|
        """
        s1 = 3
        e1 = 5
        s2 = 1
        e2 = 10

        self.assertTrue(
            _intersect_two_ranges(
                Range(start=s1, end=e1),
                Range(start=s2, end=e2),
            )
        )

    def test_both_ranges_are_equal(self):
        """
                |----|
                |----|
        """
        s1 = 5
        e1 = 10
        s2 = s1
        e2 = e1

        self.assertTrue(
            _intersect_two_ranges(
                Range(start=s1, end=e1),
                Range(start=s2, end=e2),
            )
        )

    def test_a_range_intersects_another_one_from_a_set(self):
        s1 = 10
        e1 = 13

        self.assertTrue(
            _intersect_all(
                Range(s1, e1),
                [
                    Range(1, 4),
                    Range(5, 8),
                    Range(12, 15),
                    Range(20, 24),
                ]
            )
        )

    def test_a_range_does_not_intersect_another_one_from_a_set(self):
        s1 = 10
        e1 = 13

        self.assertFalse(
            _intersect_all(
                Range(s1, e1),
                [
                    Range(1, 4),
                    Range(5, 8),
                    Range(14, 17),
                    Range(20, 24),
                ]
            )
        )
