from django.test import TestCase

from bookings.exceptions import (
    UnexistingBookingPriceCategory,
)
from bookings.models import (
    Housing,
    BookingPriceCategory,
)
from bookings.services.price_services import (
    add_price_category,
    update_price_category,
    delete_price_category,
)

class BookingSeasonServiceTests(TestCase):

    def setUp(self):
        self.housing = Housing.objects.create(name="housing 1")
        self.category = BookingPriceCategory.objects.create(housing=self.housing, name="a category")

    def test_add_a_new_price_category(self):
        category = add_price_category(housing=self.housing, name="adult")
        self.assertTrue(category)
        self.assertEqual(category.name, "adult")

    def test_update_an_unexisting_price_category(self):
        with self.assertRaises(UnexistingBookingPriceCategory):
            update_price_category(category_id=123, new_name="new name")

    def test_update_an_existing_price_category(self):
        new_name = "my new name"

        category = update_price_category(category_id=self.category.id, new_name=new_name)

        self.assertTrue(category)
        self.assertEqual(category.id, self.category.id)
        self.assertEqual(category.name, new_name)

    def test_delete_an_unexisting_price_category(self):
        with self.assertRaises(UnexistingBookingPriceCategory):
            delete_price_category(category_id=123)

    def test_delete_an_existing_price_category(self):
        delete_price_category(category_id=self.category.id)
        self.assertFalse(BookingPriceCategory.objects.filter(pk=self.category.id))
