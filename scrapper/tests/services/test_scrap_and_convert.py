from unittest import TestCase
from unittest.mock import patch

from scrapper.services import scrap_and_convert


class ScrapAndConvertTestCase(TestCase):

    @patch("scrapper.services._scrap_airbnb_data")
    def test_returns_none_on_scrap_error(self, mock_scrap):
        airbnb_id = "1234"

        mock_scrap.return_value = False

        response = scrap_and_convert(airbnb_id=airbnb_id)

        self.assertEqual(response, None)
        mock_scrap.assert_called_with(airbnb_id)

    @patch("scrapper.services._convert_airbnb_data")
    @patch("scrapper.services._scrap_airbnb_data")
    def test_returns_none_on_convert_error(self, mock_scrap, mock_convert):
        airbnb_id = "1234"
        scrapped_data = {"data": "value"}

        mock_scrap.return_value = scrapped_data
        mock_convert.return_value = None

        response = scrap_and_convert(airbnb_id=airbnb_id)

        self.assertEqual(response, None)
        mock_scrap.assert_called_with(airbnb_id)
        mock_convert.assert_called_with(scrapped_data)

    @patch("scrapper.services._convert_airbnb_data")
    @patch("scrapper.services._scrap_airbnb_data")
    def test_returns_formatted_data(self, mock_scrap, mock_convert):
        airbnb_id = "1234"
        scrapped_data = {"data": "value"}
        converted_data = {"data": "converted_value"}

        mock_scrap.return_value = scrapped_data
        mock_convert.return_value = converted_data

        response = scrap_and_convert(airbnb_id=airbnb_id)

        self.assertEqual(response, converted_data)
        mock_scrap.assert_called_with(airbnb_id)
        mock_convert.assert_called_with(scrapped_data)
