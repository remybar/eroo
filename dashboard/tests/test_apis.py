import json
from unittest import TestCase
from unittest.mock import Mock, patch

from django.test import Client
from django.urls import reverse

from ..apis import api_website_create, api_website_delete


class ApiTestCase(TestCase):

    def _check_response(self, response, expected):
        """ verify that a JSON `response` matches with the expected dictionary """
        self.assertEqual(json.loads(response), expected)

    # ---------------------------------------------------------
    # api_website_create
    # ---------------------------------------------------------

    def test_api_website_create_not_logged(self):
        """
        Redirect to the login page if the user is not logged
        """
        client = Client()
        url = reverse("api_website_create")
        login_url = reverse("account_login")
        response = client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{login_url}?next={url}")

    def test_api_website_create_is_not_ajax_request(self):
        """
        Internal server error (500) if the request is not an ajax request
        """
        request = Mock()
        request.headers = {}

        response = api_website_create(request)

        self.assertEqual(response.status_code, 500)
        self._check_response(response.content, {"error": "mauvaise requête"})

    def test_api_website_create_has_not_rental_url(self):
        """
        Internal server error (500) if the request does not contain a 'rental_url' parameter
        """
        request = Mock()
        request.headers = {"x-requested-with": "XMLHttpRequest"}
        request.POST = {}

        response = api_website_create(request)

        self.assertEqual(response.status_code, 500)
        self._check_response(response.content, {"error": "mauvaise requête"})

    def test_api_website_create_empty_rental_url(self):
        """
        Internal server error (500) if the request contains an empty 'rental_url' parameter
        """
        request = Mock()
        request.headers = {"x-requested-with": "XMLHttpRequest"}
        request.POST = {"rental_url": ""}

        response = api_website_create(request)

        self.assertEqual(response.status_code, 500)
        self._check_response(response.content, {"error": "URL de l'annonce non fournie"})

    @patch("dashboard.apis.explode_airbnb_url", Mock(return_value=(None, None)))
    def test_api_website_create_invalid_rental_url(self):
        """
        User error (400) if the request contains an invalid 'rental_url' parameter
        """
        request = Mock()
        request.headers = {"x-requested-with": "XMLHttpRequest"}
        request.POST = {"rental_url": "https://toto.fr"}

        response = api_website_create(request)

        self.assertEqual(response.status_code, 400)
        self._check_response(response.content, {"error": "L'URL fournie n'est pas une URL Airbnb valide"})

    @patch("dashboard.apis.Website.has_reached_resource_limits", Mock(return_value=True))
    @patch("dashboard.apis.explode_airbnb_url", Mock(return_value=("https://airbnb.fr", "1234")))
    def test_api_website_create_number_of_websites_exceeded(self):
        """
        User error (400) if too many websites have been generated for the current user
        """
        request = Mock()
        request.headers = {"x-requested-with": "XMLHttpRequest"}
        request.POST = {"rental_url": "https://airbnb.fr/1234"}

        response = api_website_create(request)

        self.assertEqual(response.status_code, 400)
        self._check_response(
            response.content,
            {
                "error": "Limite de nombre de sites atteinte. Supprimez-en un pour pouvoir en créer un nouveau."
            }
        )

    @patch("dashboard.apis.scrap_and_create_website")
    @patch("dashboard.apis.Website.has_reached_resource_limits", Mock(return_value=False))
    @patch("dashboard.apis.explode_airbnb_url", Mock(return_value=("https://airbnb.fr", "1234")))
    def test_api_website_create_nominal_case(self, mock_celery):
        """
        Nominal case: start a background task
        """
        mock_celery.delay().id = 121
        request = Mock()
        request.headers = {"x-requested-with": "XMLHttpRequest"}
        request.POST = {"rental_url": "https://airbnb.fr/1234"}

        response = api_website_create(request)

        self.assertEqual(response.status_code, 202)
        self._check_response(response.content, {"task_id": mock_celery.delay().id})

    # ---------------------------------------------------------
    # api_website_delete
    # ---------------------------------------------------------

    def test_api_website_delete_not_logged(self):
        """
        redirect to login url if not yet logged
        """
        client = Client()
        url = reverse("api_website_delete", args=["abcd"])
        response = client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/accounts/login/?next={url}")

    def test_api_website_delete_is_not_ajax_request(self):
        """
        Internal server error (500) if the request is not an ajax request
        """
        request = Mock()
        request.headers = {}

        response = api_website_delete(request, "1234")

        self.assertEqual(response.status_code, 500)
        self._check_response(response.content, {"error": "mauvaise requête"})

    @patch("dashboard.apis.Website.get_website", Mock(return_value=None))
    def test_api_website_delete_website_not_found(self):
        """
        User error (400) - the website identified by `key` does not exist.
        """
        request = Mock()
        request.headers = {"x-requested-with": "XMLHttpRequest"}

        response = api_website_delete(request, "1234")

        self.assertEqual(response.status_code, 400)
        self._check_response(response.content, {"error": "Ce site n'existe pas"})


    @patch("dashboard.apis.Website.get_website")
    def test_api_website_delete_nominal_case(self, mock_website):
        """
        Delete an existing website and get back the website key.
        """
        key = "1234"
        request = Mock()
        request.headers = {"x-requested-with": "XMLHttpRequest"}

        response = api_website_delete(request, key)

        mock_website.return_value.delete.assert_called()
        self.assertEqual(response.status_code, 200)
        self._check_response(response.content, {"key": key})
