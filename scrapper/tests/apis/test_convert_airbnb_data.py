from parameterized import parameterized
from unittest import TestCase
from unittest.mock import Mock

from scrapper.apis import convert_airbnb_data


class ConvertTestCase(TestCase):

    def _make_input_data(self, details, reviews):
        return ({"details": details}, {"reviews": reviews})

    def _make_expected_data(self,
        name=None, general_info=None, host=None, location=None, photos=None, description=None,
        equipments=None, reviews=None, prices=None, highlights=None, house_rules=None, rooms=None,
    ):
        return {
            "name": name,
            "general_info": general_info,
            "host": host,
            "location": location,
            "photos": photos,
            "description": description,
            "equipments": equipments,
            "reviews": reviews,
            "prices": prices,
            "highlights": highlights,
            "house_rules": house_rules,
            "rooms": rooms,
        }

    @parameterized.expand([
        (None, None),
        (tuple(), None),
        (({},), None),
        (({}, {}), None),
        (({"details: {}"}, {}), None),
    ])
    def test_returns_none_on_invalid_input_data(self, input_data, expected_data):
        response = convert_airbnb_data(input_data)
        self.assertEqual(response, expected_data)

    def test_TODO(self):
        input_data = self._make_input_data({}, {})
        expected_data = self._make_expected_data()

        response = convert_airbnb_data(input_data)
#        self.assertEqual(response, expected_data)
