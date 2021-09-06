
from unittest import TestCase
from unittest.mock import patch
from datetime import datetime
import pytz

from django.template import defaultfilters
from django.utils import timezone
from django.urls import reverse

from websites.config import WEBSITE_URL

from ..tasks import scrap_and_create_website


class TaskTestCase(TestCase):

    @patch("dashboard.tasks.scrap_and_convert")
    def test_scrap_and_create_website_scrap_exception(self, mock_scrap):
        """
        Data scrapping raises an exception
        """
        user_id = 123
        base_url = "https://airbnb.fr"
        airbnb_id = "123456"

        mock_scrap.side_effect = Exception()

        response = scrap_and_create_website(user_id, base_url, airbnb_id)

        self.assertEqual(response, {"result": "error", "msg": "Impossible d'accéder à votre annonce Airbnb"})
        mock_scrap.assert_called_with(airbnb_id)

    @patch("dashboard.tasks.scrap_and_convert")
    def test_scrap_and_create_website_scrap_error(self, mock_scrap):
        """
        Data scraping returns an error
        """
        user_id = 123
        base_url = "https://airbnb.fr"
        airbnb_id = "123456"

        mock_scrap.return_value = False

        response = scrap_and_create_website(user_id, base_url, airbnb_id)

        self.assertEqual(response, {"result": "error", "msg": "Impossible d'accéder à votre annonce Airbnb"})
        mock_scrap.assert_called_with(airbnb_id)

    @patch("dashboard.tasks.Website.create")
    @patch("dashboard.tasks.scrap_and_convert")
    def test_scrap_and_create_website_create_raise_exception(self, mock_scrap, mock_create):
        """
        Website creation raises an exception
        """
        user_id = 123
        base_url = "https://airbnb.fr"
        airbnb_id = "123456"
        scrapped_data = {"data": "value"}

        mock_scrap.return_value = scrapped_data
        mock_create.side_effect = Exception()

        response = scrap_and_create_website(user_id, base_url, airbnb_id)

        self.assertEqual(response, {"result": "error", "msg": "Impossible de créer le site web à partir des données de votre annonce"})
        mock_scrap.assert_called_with(airbnb_id)
        mock_create.assert_called_with(user_id, base_url, scrapped_data)

    @patch("dashboard.tasks.Website.create")
    @patch("dashboard.tasks.scrap_and_convert")
    def test_scrap_and_create_website_create_error(self, mock_scrap, mock_create):
        """
        Website creation returns an error
        """
        user_id = 123
        base_url = "https://airbnb.fr"
        airbnb_id = "123456"
        scrapped_data = {"data": "value"}

        mock_scrap.return_value = scrapped_data
        mock_create.return_value = None

        response = scrap_and_create_website(user_id, base_url, airbnb_id)

        self.assertEqual(response, {"result": "error", "msg": "Impossible de créer le site web à partir des données de votre annonce"})
        mock_scrap.assert_called_with(airbnb_id)
        mock_create.assert_called_with(user_id, base_url, scrapped_data)

    @patch("dashboard.tasks.Website.create")
    @patch("dashboard.tasks.scrap_and_convert")
    def test_scrap_and_create_website_nominal_case(self, mock_scrap, mock_create):
        """
        Website creation returns an error
        """
        user_id = 123
        base_url = "https://airbnb.fr"
        airbnb_id = "123456"
        scrapped_data = {"data": "value"}
        website_data = {
            "key": "1234",
            "name": "My website",
            "generated_date": datetime(2009, 7, 10, 18, 44, 59, 193982, tzinfo=pytz.utc),
        }

        mock_scrap.return_value = scrapped_data
        mock_create.return_value.configure_mock(**website_data)

        response = scrap_and_create_website(user_id, base_url, airbnb_id)

        self.assertEqual(
            response,
            {
                "result": "success",
                "key": website_data["key"],
                "name": website_data["name"],
                "url": WEBSITE_URL % website_data["key"],
                "generated_date": defaultfilters.date(timezone.localtime(website_data["generated_date"]), "d/m/Y G:i"),
                "delete_url": reverse('api_website_delete', args=[website_data["key"]]),

            }
        )
        mock_scrap.assert_called_with(airbnb_id)
        mock_create.assert_called_with(user_id, base_url, scrapped_data)
