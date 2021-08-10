from parameterized import parameterized
from unittest import TestCase
from unittest.mock import Mock, patch, call

from django.core.files import File

from websites.models import (
    Website,
    WebsitePhoto,
    KEY_LENGTH
)
from websites.config import MAX_WEBSITES_COUNT


class ModelTestCase(TestCase):

    filename = "myfile.jpg"
    url = f"https://my-media.fr/{filename}?debug=1"
    caption = "my caption"
    image_content = [1, 2, 3, 4]

    @patch('websites.models.Website.objects.get')
    def test_get_website_key_does_not_exist(self, mock_get):
        mock_get.return_value = None
        result = Website.get_website("1234")
        self.assertEqual(result, None)

    @patch('websites.models.Website.objects.get')
    def test_get_website_key_exists(self, mock_get):
        fake_website = {"id": 1}
        mock_get.return_value = fake_website
        result = Website.get_website("1234")
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
        self.assertEqual(Website.has_reached_resource_limits(1), expected)
        mock_filter.assert_called_once_with(user=1)

    @patch('websites.models.Website.objects.filter.return_value.count')
    @patch('websites.models.Website.objects.filter')
    @patch('websites.models.ShortUUID.random')
    def test_generate_key_that_does_not_exist_yet(self, mock_uuid, mock_filter, mock_count):
        mock_uuid.return_value = "1234"
        mock_count.return_value = 0

        key = Website._generate_key()
        self.assertEqual(key, "1234")
        mock_uuid.assert_called_once_with(length=KEY_LENGTH)
        mock_filter.assert_called_once_with(key="1234")

    @patch('websites.models.Website.objects.filter.return_value.count')
    @patch('websites.models.Website.objects.filter')
    @patch('websites.models.ShortUUID.random')
    def test_generate_key_that_already_exists(self, mock_uuid, mock_filter, mock_count):
        mock_uuid.side_effect = ["1234", "5678"]
        mock_count.side_effect = [1, 0]

        key = Website._generate_key()
        self.assertEqual(key, "5678")
        mock_uuid.assert_called_with(length=KEY_LENGTH)
        mock_filter.assert_has_calls([call(key="1234"), call(key="5678")])

    @parameterized.expand([
        ([], ""),
        (["line 1"], "<p>line 1</p>"),
        (["line 1", "line 2"], "<p>line 1</p>\n<p>line 2</p>"),
        (["line 1", "", "line 2"], "<p>line 1</p>\n<br />\n<p>line 2</p>"),
        (["<li>line</li>"], "<p>&lt;li&gt;line&lt;/li&gt;</p>"),
    ])
    def test_generate_description(self, input_value, expected_value):
        self.assertEqual(Website._generate_description(input_value), expected_value)

    @parameterized.expand([
        ([],),
        ([{}],),
        ([{"url": "toto"}],),
        ([{"caption": "toto"}],),
    ])
    @patch('websites.models.website.download_media_file')
    def test_create_photos_error_cases(self, photos, mock_download):
        website = Mock(spec=Website)
        Website._create_photos(website, photos)
        website._create_photo.assert_not_called()
        mock_download.assert_not_called()

    @patch('websites.models.website.download_media_file')
    def test_create_photos_one_photo_download_error(self, mock_download):
        website = Mock(spec=Website)
        mock_download.return_value = False

        Website._create_photos(website, [{"url": self.url, "caption": self.caption}])

        mock_download.assert_called_once_with(self.url, self.filename)
        website._create_photo.assert_not_called()

    @patch('websites.models.website.download_media_file')
    def test_create_photos_one_photo_download_success(self, mock_download):

        website = Mock(spec=Website)
        mock_download.return_value = self.image_content

        Website._create_photos(website, [{"url": self.url, "caption": self.caption}])

        mock_download.assert_called_once_with(self.url, self.filename)
        website._create_photo.assert_called_once_with(self.filename, self.image_content, self.caption)

    @patch('websites.models.website.download_media_file')
    def test_create_photos_several_photos(self, mock_download):
        website = Mock(spec=Website)
        photos_content = []
        photos = []
        expected_download_calls = []
        expected_photo_calls = []
        for i in range(4):
            filename = f"file_{i}.jpg"
            url = f"https://media.fr/{filename}?debug=1"
            caption = f"caption_{i}"
            content = [i * v for v in self.image_content]
            photos_content.append(content)
            photos.append({"url": url, "caption": caption})
            expected_download_calls.append(call(url, filename))
            expected_photo_calls.append(call(filename, content, caption))

        mock_download.side_effect = photos_content

        Website._create_photos(website, photos)

        mock_download.assert_has_calls(expected_download_calls)
        website._create_photo.assert_has_calls(expected_photo_calls)

    @patch('websites.models.WebsitePhoto.objects.create')
    def test_create_photo(self, mock_photo):
        website = Mock(spec=Website)
        photo = Mock(spec=WebsitePhoto)
        mock_photo.return_value = photo

        Website._create_photo(website, "filename", [1, 2, 3], "caption")
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
