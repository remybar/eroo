import logging
from unittest import TestCase
from unittest.mock import patch

from django.conf import settings

from scrapper.apis import scrap_airbnb_data


class ScrapTestCase(TestCase):

    @patch("scrapper.apis.airbnb.Api")
    def test_returns_none_when_airbnb_api_exception(self, mock_api):
        logging.disable(logging.CRITICAL)
        
        airbnb_id = "1234"
        mock_api.side_effect = Exception()

        response = scrap_airbnb_data(airbnb_id)

        self.assertEqual(response, None)
        mock_api.assert_called_with(
            randomize=True,
            api_key=settings.AIRBNB_API_KEY,
            currency="EUR",
            locale="fr",
            country="fr",
            language="fr-fr",
            proxy=None,
        )

    @patch("scrapper.apis.airbnb.Api")
    def test_returns_scrapped_data(self, mock_api):
        airbnb_id = "1234"
        details = {"data": "details"}
        reviews = {"data": "reviews"}

        mock_api.return_value.get_listing_details.return_value = details
        mock_api.return_value.get_reviews.return_value = reviews

        response = scrap_airbnb_data(airbnb_id)

        self.assertEqual(response, (details, reviews))
        mock_api.assert_called_with(
            randomize=True,
            api_key=settings.AIRBNB_API_KEY,
            currency="EUR",
            locale="fr",
            country="fr",
            language="fr-fr",
            proxy=None,
        )
        mock_api.return_value.get_listing_details.assert_called_with(airbnb_id)
        mock_api.return_value.get_reviews.assert_called_with(airbnb_id)
