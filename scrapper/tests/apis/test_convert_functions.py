from parameterized import parameterized
from unittest import TestCase

from scrapper.apis import (
    _get_airbnb_name,
    _get_airbnb_host_info,
    _get_airbnb_general_info,
    _get_airbnb_location,
    _get_airbnb_photos,
    _get_airbnb_description,
    _get_airbnb_equipment_areas,
    _get_airbnb_equipments,
    _get_airbnb_equipments_per_area,
    _get_airbnb_reviews,
    _get_airbnb_prices,
    _get_airbnb_highlights,
    _get_airbnb_house_rules,
    _get_airbnb_rooms,
)
from .common import (
    _in_host_info, _out_host_info, nominal_host_info, expected_nominal_host_info,
    _in_general_info, _out_general_info, nominal_general_info, expected_general_info,
    _in_location, _out_location, nominal_location, expected_location,
    _in_photos, _out_photos, nominal_photos, expected_photos,
    _in_areas, _in_area, nominal_areas, expected_areas,
    _in_equipments, _in_equipment, _out_equipment, nominal_equipments, expected_equipments,
    input_equipments_per_areas, expected_equipments_per_areas,
    _in_price, _out_price, nominal_prices, expected_prices,
    _in_highlight, _out_highlight, nominal_highlights, expected_highlights,
    _in_room, _out_room, nominal_rooms, expected_rooms,
    nominal_review, expected_review
)


class ConvertFunctionsTestCase(TestCase):

    @parameterized.expand([
        (None, None),
        ({}, None),
        ({"p3_summary_title": "my_name"}, "my_name"),
    ])
    def test_get_airbnb_name(self, input, expected):
        self.assertEqual(_get_airbnb_name(input), expected)

    @parameterized.expand([
        (None, None),
        ({}, None),
        ({"primary_host": {}}, _out_host_info()),
        (_in_host_info(name="my_name"), _out_host_info(name="my_name")),
        (_in_host_info(picture_large_url="my_url"), _out_host_info(url="my_url")),
        (_in_host_info(about="my_description"), _out_host_info(description="my_description")),
        (_in_host_info(languages="my_languages"), _out_host_info(languages="my_languages")),
        (nominal_host_info, expected_nominal_host_info),
    ])
    def test_get_airbnb_host_info(self, input, expected):
        self.assertEqual(_get_airbnb_host_info(input), expected)

    @parameterized.expand([
        (None, None),
        ({}, _out_general_info()),
        (_in_general_info(), _out_general_info()),
        (_in_general_info(bathroom_label="1"), _out_general_info(bathroom="1")),
        (_in_general_info(bathroom_label="1 1"), _out_general_info(bathroom="1")),
        (_in_general_info(bathroom_label="1.5"), _out_general_info(bathroom="1")),
        (_in_general_info(bathroom_label="1,8"), _out_general_info(bathroom="1")),
        (_in_general_info(bed_label="1"), _out_general_info(bed="1")),
        (_in_general_info(bedroom_label="1"), _out_general_info(bedroom="1")),
        (_in_general_info(guest_label="1"), _out_general_info(guest="1")),
        (nominal_general_info, expected_general_info)
    ])
    def test_get_airbnb_general_info(self, input, expected):
        self.assertEqual(_get_airbnb_general_info(input), expected)

    @parameterized.expand([
        (None, None),
        ({}, _out_location()),
        (_in_location(location_title="my_title"), _out_location(title="my_title")),
        (_in_location(lat="12.34"), _out_location(lat="12.34")),
        (_in_location(lng="56.78"), _out_location(lng="56.78")),
        (nominal_location, expected_location),
    ])
    def test_get_airbnb_location(self, input, expected):
        self.assertEqual(_get_airbnb_location(input), expected)

    @parameterized.expand([
        (None, None),
        ({}, None),
        ({"toto": []}, None),
        ({"photos": [_in_photos(large="my_url")]}, [_out_photos(url="my_url")]),
        ({"photos": [_in_photos(large="my_url?toto")]}, [_out_photos(url="my_url")]),
        ({"photos": [_in_photos(caption="my_caption")]}, [_out_photos(caption="my_caption")]),
        (nominal_photos, expected_photos)
    ])
    def test_get_airbnb_photos(self, input, expected):
        self.assertEqual(_get_airbnb_photos(input), expected)

    @parameterized.expand([
        (None, None),
        ({}, None),
        ({"sectioned_description": {}}, None),
        ({"sectioned_description": {"description": ""}}, [""]),
        ({"sectioned_description": {"description": "aaa"}}, ["aaa"]),
        ({"sectioned_description": {"description": "aaa\nbbb\ncccc"}}, ["aaa", "bbb", "cccc"]),
    ])
    def test_get_airbnb_description(self, input, expected):
        self.assertEqual(_get_airbnb_description(input), expected)

    @parameterized.expand([
        (None, []),
        ({}, []),
        ({"toto": "xxx"}, []),
        (_in_areas([]), []),
        (_in_areas([_in_area(title="my_title")]), []),
        (_in_areas([_in_area(amenity_ids=[])]), []),
        (_in_areas([_in_area(title="my_title", amenity_ids=[])]), []),
        (nominal_areas, expected_areas),
    ])
    def test_get_airbnb_equipment_areas(self, input, expected):
        self.assertEqual(_get_airbnb_equipment_areas(input), expected)

    @parameterized.expand([
        (None, {}),
        ({}, {}),
        ({"toto": "xxx"}, {}),
        (_in_equipments([]), {}),
        (_in_equipments([_in_equipment(id=1)]), {}),
        (_in_equipments([_in_equipment(name="eq1")]), {}),
        (_in_equipments([_in_equipment(description="desc1")]), {}),
        (_in_equipments([_in_equipment(id=1, name="eq1")]), {}),
        (_in_equipments([_in_equipment(id=1, description="desc1")]), {}),
        (_in_equipments([_in_equipment(name="eq1", description="desc1")]), {}),
        (
            _in_equipments([_in_equipment(id=1, name="eq1", description="desc1")]),
            {"1": _out_equipment(name="eq1", description="desc1")}
        ),
        (nominal_equipments, expected_equipments),
    ])
    def test_get_airbnb_equipments(self, input, expected):
        self.assertEqual(_get_airbnb_equipments(input), expected)

    @parameterized.expand([
        (None, {}),
        ({}, {}),
        ({"toto": "xxx"}, {}),
        ({"see_all_amenity_sections": []}, {}),
        ({"listing_amenities": []}, {}),
        ({"see_all_amenity_sections": [], "listing_amenities": []}, {}),
        (input_equipments_per_areas, expected_equipments_per_areas)
    ])
    def test_get_airbnb_equipments_per_area(self, input, expected):
        self.assertEqual(_get_airbnb_equipments_per_area(input), expected)

    @parameterized.expand([
        (None, []),
        ({}, []),
        ({"toto": "xxx"}, []),
        ({"price_details": []}, []),
        ({"price_details": [_in_price(label="mylabel")]}, []),
        ({"price_details": [_in_price(value="10.5")]}, []),
        (
            {"price_details": [_in_price(label="mylabel", value="10.5")]},
            [_out_price(label="mylabel", value="10.5")],
        ),
        (nominal_prices, expected_prices)
    ])
    def test_get_airbnb_prices(self, input, expected):
        self.assertEqual(_get_airbnb_prices(input), expected)

    @parameterized.expand([
        (None, []),
        ({}, []),
        ({"toto": "xxx"}, []),
        ({"highlights": []}, []),
        ({"highlights": [_in_highlight(headline="headline")]}, []),
        ({"highlights": [_in_highlight(message="message")]}, []),
        (
            {"highlights": [_in_highlight(headline="headline", message="message")]},
            [_out_highlight(headline="headline", message="message")]
        ),
        (nominal_highlights, expected_highlights)
    ])
    def test_get_airbnb_highlights(self, input, expected):
        self.assertEqual(_get_airbnb_highlights(input), expected)

    @parameterized.expand([
        (None, []),
        ({}, []),
        ({"toto": "xxx"}, []),
        ({"guest_controls": "xxx"}, []),
        ({"guest_controls": {"structured_house_rules": []}}, []),
        ({"guest_controls": {"structured_house_rules": [1, 2, 3]}}, [1, 2, 3]),
    ])
    def test_get_airbnb_house_rules(self, input, expected):
        self.assertEqual(_get_airbnb_house_rules(input), expected)

    @parameterized.expand([
        (None, []),
        ({}, []),
        ({"toto": "xxx"}, []),
        ({"hometour_rooms": []}, []),
        ({"hometour_rooms": [_in_room(name_with_type="name")]}, []),
        ({"hometour_rooms": [_in_room(highlights_hometour="details")]}, []),
        (
            {"hometour_rooms": [_in_room(name_with_type="name", highlights_hometour="details")]},
            [_out_room(name="name", details="details")],
        ),
        (nominal_rooms, expected_rooms)
    ])
    def test_get_airbnb_rooms(self, input, expected):
        self.assertEqual(_get_airbnb_rooms(input), expected)

    @parameterized.expand([
        (None, []),
        ([{"rating": 5}], []),
        ([{"author": "a"}], []),
        ([{"author": {"has_profile_pic": True}}], []),
        ([{"author": {"first_name": "f"}}], []),
        ([{"author": {"picture_url": "f"}}], []),
        ([{"comments": "c"}], []),
        ([{"created_at": "2001T10"}], []),
        ([{"language": "c"}], []),
        ([nominal_review | {"rating": 4}], []),
        ([nominal_review], [expected_review]),
        ([
            nominal_review | {"comments": "1"},
            nominal_review | {"comments": "2", "rating": 4},
            nominal_review | {"comments": "3"},
         ],
         [
             expected_review | {"review": "1"},
             expected_review | {"review": "3"},
        ]),
        (
            [
                nominal_review | {"comments": "1", "created_at": "2006-05-04T01-01"},
                nominal_review | {"comments": "2", "created_at": "2001-05-04T01-01"},
                nominal_review | {"comments": "3", "created_at": "2004-05-04T01-01"},
                nominal_review | {"comments": "4", "created_at": "2003-05-04T01-01"},
                nominal_review | {"comments": "5", "created_at": "2008-05-04T01-01"},
                nominal_review | {"comments": "6", "created_at": "2002-05-04T01-01"},
            ],
            [
                expected_review | {"review": "5", "date": "2008-05-04"},
                expected_review | {"review": "1", "date": "2006-05-04"},
                expected_review | {"review": "3", "date": "2004-05-04"},
                expected_review | {"review": "4", "date": "2003-05-04"},
                expected_review | {"review": "6", "date": "2002-05-04"},
            ]
        ),
    ])
    def test_get_airbnb_reviews(self, input, expected):
        self.assertEqual(_get_airbnb_reviews(input), expected)
