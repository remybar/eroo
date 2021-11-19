from parameterized import parameterized
from unittest import TestCase
from unittest.mock import Mock, patch, call

from allauth.utils import get_user_model

from websites.config import MAX_WEBSITES_COUNT

from websites.selectors import (
    get_website,
    has_reached_resource_limits,
    generate_website_key,
    WEBSITE_KEY_LENGTH,
)

User = get_user_model()

class SelectorsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SelectorsTestCase, cls).setUpClass()
        cls.user = User.objects.get_or_create(username='Test User')

    @patch('websites.models.Website.objects.get')
    def test_get_website_key_does_not_exist(self, mock_get):
        mock_get.return_value = None
        result = get_website(key="1234")
        self.assertEqual(result, None)

    @patch('websites.models.Website.objects.get')
    def test_get_website_key_exists(self, mock_get):
        fake_website = {"id": 1}
        mock_get.return_value = fake_website
        result = get_website(key="1234")
        self.assertEqual(result, fake_website)

    @parameterized.expand([
        (MAX_WEBSITES_COUNT, True),
        (MAX_WEBSITES_COUNT + 1, True),
        (MAX_WEBSITES_COUNT - 1, False),
    ])
    @patch('websites.models.Website.objects.filter.return_value.count')
    @patch('websites.models.Website.objects.filter')
    def test_has_reached_resource_limits(self, input_value, expected, mock_filter, mock_count):
        mock_count.return_value = input_value
        self.assertEqual(has_reached_resource_limits(user=self.user), expected)
        mock_filter.assert_called_once_with(user=self.user)

    @patch('websites.models.Website.objects.filter.return_value.count')
    @patch('websites.models.Website.objects.filter')
    @patch('websites.selectors.ShortUUID.random')
    def test_generate_key_that_does_not_exist_yet(self, mock_uuid, mock_filter, mock_count):
        mock_uuid.return_value = "1234"
        mock_count.return_value = 0

        key = generate_website_key()
        self.assertEqual(key, "1234")
        mock_uuid.assert_called_once_with(length=WEBSITE_KEY_LENGTH)
        mock_filter.assert_called_once_with(key="1234")

    @patch('websites.models.Website.objects.filter.return_value.count')
    @patch('websites.models.Website.objects.filter')
    @patch('websites.selectors.ShortUUID.random')
    def test_generate_key_that_already_exists(self, mock_uuid, mock_filter, mock_count):
        mock_uuid.side_effect = ["1234", "5678"]
        mock_count.side_effect = [1, 0]

        key = generate_website_key()
        self.assertEqual(key, "5678")
        mock_uuid.assert_called_with(length=WEBSITE_KEY_LENGTH)
        mock_filter.assert_has_calls([call(key="1234"), call(key="5678")])
