from unittest import TestCase
from unittest.mock import Mock, patch

from django.test import Client
from django.urls import reverse

from ..views import DeleteAccountView


class ViewTestCase(TestCase):

    def assertStatusCode(self, category, value):
        statusCodeChecking = {
            'info': (100, 199),
            'success': (200, 299),
            'redirection': (300, 399),
            'client_error': (400, 499),
            'server_error': (500, 599),
        }
        low, high = statusCodeChecking[category]
        self.assertIn(value, range(low, high + 1))

    def test_delete_account_not_logged(self):
        """
        Try to delete an account without being logged
        """
        client = Client()
        url = reverse("account_delete")
        login_url = reverse("account_login")
        response = client.post(url)

        self.assertStatusCode('redirection', response.status_code)

TODO RBA: to fix
#        self.assertEqual(response.url, f"{login_url}?next={url}")

    @patch("accounts.views.User.objects.get", Mock(return_value=None))
    def test_delete_account_not_exist(self):
        """
        Try to delete an account that does not exist
        """
        view = DeleteAccountView()

        request = Mock()
        request.META = {"CSRF_COOKIE": "XXX"}
        response = view.post(request)

        self.assertStatusCode('success', response.status_code)

    @patch("accounts.views.User.objects.get")
    @patch("accounts.views.logout")
    def test_delete_account_exist(self, mock_logout, mock_get):
        """
        Try to delete an account that does not exist
        """
        view = DeleteAccountView()

        request = Mock()
        request.META = {"CSRF_COOKIE": "XXX"}
        response = view.post(request)

        mock_get.return_value.delete.assert_called()
        mock_logout.assert_called()
        self.assertStatusCode('redirection', response.status_code)
        self.assertEqual(response.url, "/")
