from parameterized import parameterized
from unittest import TestCase

from scrapper.services import _convert_airbnb_data

from .common import full_input_details, full_input_reviews, full_converted_data


class ConvertTestCase(TestCase):

    @parameterized.expand([
        (None, None),
        (tuple(), None),
        (({},), None),
        (({}, {}), None),
        (({"pdp_listing_detail": {}}, {}), None),
        (({}, {"reviews": {}}), None),
        (({"pdp_listing_detail": {}}, {"reviews": {}}), None),
        ((full_input_details, full_input_reviews), full_converted_data),
        ((
            full_input_details | {"pdp_listing_detail": {"p3_summary_title": None}},
            full_input_reviews
         ), None)
    ])
    def test_returns_none_on_invalid_input_data(self, input_data, expected_data):
        response = _convert_airbnb_data(input_data)
        self.assertEqual(response, expected_data)
