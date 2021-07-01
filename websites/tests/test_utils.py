from unittest.mock import patch
from unittest import TestCase
import requests

from websites.utils import explode_airbnb_url


class UtilsTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_airnb_id_from_valid_url(self):
        """
        When the airbnb URL is valid, correctly extract the airbnb id
        """
        url = "https://fr.airbnb.be/rooms/23938383?translate_ugc=false&federated_search_id=838cfd1f-11b1-4c8b-a68f-2555b8cf3820&source_impression_id=p3_1624950929_TcLTRXRwLWiECk8t"  # noqa: E501

        base_url, airbnb_id = explode_airbnb_url(url)

        self.assertEqual(base_url, "https://fr.airbnb.be/rooms/23938383")
        self.assertEqual(airbnb_id, "23938383")

    @patch("websites.utils.requests.get")
    def test_get_airnb_id_from_valid_but_shortcut_url(self, mock_get):
        """
        When the airbnb URL is valid but is a shortcut of the real url, correctly extract the airbnb id
        """
        shortcut_url = "https://myshortcuturl.be"
        real_url = "https://fr.airbnb.be/rooms/23938383?translate_ugc=false&federated_search_id=838cfd1f-11b1-4c8b-a68f-2555b8cf3820&source_impression_id=p3_1624950929_TcLTRXRwLWiECk8t"  # noqa: E501
        mock_get.return_value.status_code = 200
        mock_get.return_value.url = real_url

        base_url, airbnb_id = explode_airbnb_url(shortcut_url)

        self.assertEqual(base_url, "https://fr.airbnb.be/rooms/23938383")
        self.assertEqual(airbnb_id, "23938383")

    @patch("websites.utils.requests.get")
    def test_get_airnb_id_from_invalid_url(self, mock_get):
        """
        When the airbnb URL is not valid, returns None
        """
        url = "https://myshortcuturl.be?azezeazkezaekl"
        mock_get.return_value.status_code = 200
        mock_get.return_value.url = url

        base_url, airbnb_id = explode_airbnb_url(url)

        self.assertEqual(base_url, None)
        self.assertEqual(airbnb_id, None)

    @patch("websites.utils.requests.get")
    def test_get_airnb_id_from_requests_error(self, mock_get):
        """
        When the airbnb shortcut URL does not exist
        """
        shortcut_url = "https://myshortcuturl.be"
        mock_get.return_value.status_code = 404
        mock_get.return_value.url = shortcut_url

        base_url, airbnb_id = explode_airbnb_url(shortcut_url)

        self.assertEqual(base_url, None)
        self.assertEqual(airbnb_id, None)

    @patch("websites.utils.requests.get")
    def test_get_airnb_id_but_requests_timeout(self, mock_get):
        """
        When the airbnb shortcut URL access timeout
        """
        shortcut_url = "https://myshortcuturl.be"
        mock_get.side_effect = requests.exceptions.Timeout()

        base_url, airbnb_id = explode_airbnb_url(shortcut_url)

        self.assertEqual(base_url, None)
        self.assertEqual(airbnb_id, None)
