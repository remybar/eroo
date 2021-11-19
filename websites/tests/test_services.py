import requests
from parameterized import parameterized
from unittest import TestCase
from unittest.mock import Mock, patch, call, ANY

from django.core.files import File

from websites.models import (
    Website,
    WebsitePhoto,
    KEY_LENGTH
)
from websites.config import MAX_WEBSITES_COUNT
from websites.services import (
    _explode_airbnb_url,
    _generate_website_description,
    _create_photo,
    create_photos,
)

class ServicesTestCase(TestCase):

    filename = "myfile.jpg"
    url = f"https://my-media.fr/{filename}?debug=1"
    caption = "my caption"
    image_content = [1, 2, 3, 4]

    def test_get_airnb_id_from_valid_url(self):
        """
        When the airbnb URL is valid, correctly extract the airbnb id
        """
        url = "https://fr.airbnb.be/rooms/23938383?translate_ugc=false&federated_search_id=838cfd1f-11b1-4c8b-a68f-2555b8cf3820&source_impression_id=p3_1624950929_TcLTRXRwLWiECk8t"  # noqa: E501

        base_url, airbnb_id = _explode_airbnb_url(url=url)

        self.assertEqual(base_url, "https://fr.airbnb.be/rooms/23938383")
        self.assertEqual(airbnb_id, "23938383")

    @patch("common.services.requests.get")
    def test_get_airnb_id_from_valid_but_shortcut_url(self, mock_get):
        """
        When the airbnb URL is valid but is a shortcut of the real url, correctly extract the airbnb id
        """
        shortcut_url = "https://myshortcuturl.be"
        real_url = "https://fr.airbnb.be/rooms/23938383?translate_ugc=false&federated_search_id=838cfd1f-11b1-4c8b-a68f-2555b8cf3820&source_impression_id=p3_1624950929_TcLTRXRwLWiECk8t"  # noqa: E501
        mock_get.return_value.status_code = 200
        mock_get.return_value.url = real_url

        base_url, airbnb_id = _explode_airbnb_url(url=shortcut_url)

        self.assertEqual(base_url, "https://fr.airbnb.be/rooms/23938383")
        self.assertEqual(airbnb_id, "23938383")

    @patch("common.services.requests.get")
    def test_get_airnb_id_from_invalid_url(self, mock_get):
        """
        When the airbnb URL is not valid, returns None
        """
        url = "https://myshortcuturl.be?azezeazkezaekl"
        mock_get.return_value.status_code = 200
        mock_get.return_value.url = url

        base_url, airbnb_id = _explode_airbnb_url(url=url)

        self.assertEqual(base_url, None)
        self.assertEqual(airbnb_id, None)

    @patch("common.services.requests.get")
    def test_get_airnb_id_from_requests_error(self, mock_get):
        """
        When the airbnb shortcut URL does not exist
        """
        shortcut_url = "https://myshortcuturl.be"
        mock_get.return_value.status_code = 404
        mock_get.return_value.url = shortcut_url

        base_url, airbnb_id = _explode_airbnb_url(url=shortcut_url)

        self.assertEqual(base_url, None)
        self.assertEqual(airbnb_id, None)

    @patch("common.services.requests.get")
    def test_get_airnb_id_but_requests_timeout(self, mock_get):
        """
        When the airbnb shortcut URL access timeout
        """
        shortcut_url = "https://myshortcuturl.be"
        mock_get.side_effect = requests.exceptions.Timeout()

        base_url, airbnb_id = _explode_airbnb_url(url=shortcut_url)

        self.assertEqual(base_url, None)
        self.assertEqual(airbnb_id, None)

    @parameterized.expand([
        ([], ""),
        (["line 1"], "<p>line 1</p>"),
        (["line 1", "line 2"], "<p>line 1</p>\n<p>line 2</p>"),
        (["line 1", "", "line 2"], "<p>line 1</p>\n<br />\n<p>line 2</p>"),
        (["<li>line</li>"], "<p>&lt;li&gt;line&lt;/li&gt;</p>"),
    ])
    def test_generate_description(self, input_value, expected_value):
        self.assertEqual(_generate_website_description(desc_lines=input_value), expected_value)

    @parameterized.expand([
        ([],),
        ([{}],),
        ([{"url": "toto"}],),
        ([{"caption": "toto"}],),
    ])
    @patch('websites.services.download_media_file')
    @patch('websites.services.WebsitePhoto.objects.create')
    def test_create_photos_error_cases(self, photos, mock_create, mock_download):
        website = Mock(spec=Website)
        create_photos(website=website, data=photos)

        mock_download.assert_not_called()
        mock_create.assert_not_called()

    @patch('websites.services.download_media_file')
    @patch('websites.services.WebsitePhoto.objects.create')
    def test_create_photos_one_photo_download_error(self, mock_create, mock_download):
        website = Mock(spec=Website)
        mock_download.return_value = False

        create_photos(website=website, data=[{"url": self.url, "caption": self.caption}])

        mock_download.assert_called_once_with(self.url, self.filename)
        mock_create.assert_not_called()

    @patch('websites.services.download_media_file')
    @patch('websites.services.WebsitePhoto.objects.create')
    def test_create_photos_one_photo_download_success(self, mock_create, mock_download):

        website = Mock(spec=Website)
        photo = Mock(spec=WebsitePhoto)
        mock_download.return_value = self.image_content
        mock_create.return_value = photo

        create_photos(website=website, data=[{"url": self.url, "caption": self.caption}])

        mock_download.assert_called_once_with(self.url, self.filename)
        mock_create.assert_called_once_with(caption=self.caption, website=website)
        photo.save.assert_called_once()

    @patch('websites.services.download_media_file')
    @patch('websites.services.WebsitePhoto.objects.create')
    def test_create_photos_several_photos(self, mock_create, mock_download):
        website = Mock(spec=Website)
        photo = Mock(spec=WebsitePhoto)

        photos_content = []
        photos = []
        expected_download_calls = []
        expected_create_calls = []
        expected_image_save_calls = []
        for i in range(4):
            filename = f"file_{i}.jpg"
            url = f"https://media.fr/{filename}?debug=1"
            caption = f"caption_{i}"
            content = [i * v for v in self.image_content]
            photos_content.append(content)
            photos.append({"url": url, "caption": caption})
            expected_download_calls.append(call(url, filename))
            expected_create_calls.append(call(caption=caption, website=website))
            expected_image_save_calls.append(call(filename, ANY))  # TODO BAR: replace ANY by a mock of File(content)

        mock_download.side_effect = photos_content
        mock_create.return_value = photo

        create_photos(website=website, data=photos)

        mock_download.assert_has_calls(expected_download_calls, any_order=True)
        mock_create.assert_has_calls(expected_create_calls, any_order=True)
        photo.image.save.assert_has_calls(expected_image_save_calls, any_order=True)

    @patch('websites.models.WebsitePhoto.objects.create')
    def test_create_photo(self, mock_photo):
        website = Mock(spec=Website)
        photo = Mock(spec=WebsitePhoto)
        mock_photo.return_value = photo

        _create_photo(website=website, filename="filename", content=[1, 2, 3], caption="caption")
        mock_photo.assert_called_once_with(caption="caption", website=website)
#        photo.image.save.assert_called_once_with("filename", File([1, 2, 3]))
        photo.save.assert_has_calls([call()])

    # _create_reviews
    # _create_location
    # _create_host
    # _create_equipments
    # _create_highlights
    # _create_rules
    # _create_rooms
    # create
