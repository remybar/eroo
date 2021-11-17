from parameterized import parameterized
from unittest import TestCase

from scrapper.services import _validate_data

from .common import full_converted_data


class ValidateDataTestCase(TestCase):

    @parameterized.expand([
        (None, None),
        (full_converted_data, full_converted_data),
        (full_converted_data | {"name": None}, None),
        (full_converted_data | {"description": None}, None)
    ])
    def test_(self, input, expected):
        self.assertEqual(_validate_data(input), expected)
