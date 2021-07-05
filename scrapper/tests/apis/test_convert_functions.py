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


# ----------------------------------------------------
# utility functions
# ----------------------------------------------------

def _in_host_info(**kwargs):
    return {"primary_host": kwargs}


def _out_host_info(name=None, url=None, description=None, languages=None):
    return {
        "name": name,
        "picture_url": url,
        "description": description,
        "languages": languages
    }


nominal_host_info = _in_host_info(
    name="my_name",
    picture_large_url="my_url",
    about="my_description",
    languages="my_languages"
)
expected_nominal_host_info = _out_host_info(
    name="my_name",
    url="my_url",
    description="my_description",
    languages="my_languages"
)


def _in_general_info(**kwargs):
    return kwargs


def _out_general_info(bathroom=None, bed=None, bedroom=None, guest=None):
    return {
        "bathroom_count": bathroom,
        "bed_count": bed,
        "bedroom_count": bedroom,
        "guest_count": guest,
    }


nominal_general_info = _in_general_info(
    bathroom_label="1",
    bed_label="2",
    bedroom_label="3",
    guest_label="4"
)
expected_general_info = _out_general_info(bathroom="1", bed="2", bedroom="3", guest="4")


def _in_location(**kwargs):
    return kwargs


def _out_location(title=None, lat=None, lng=None):
    return {
        "title": title,
        "coords": {"lat": lat, "lng": lng}
    }


nominal_location = _in_location(location_title="my_title", lat="12.34", lng="56.78")
expected_location = _out_location(title="my_title", lat="12.34", lng="56.78")


def _in_photos(**kwargs):
    return kwargs


def _out_photos(url=None, caption=None):
    return {"url": url, "caption": caption}


nominal_photos = {
    "photos": [
        _in_photos(large="my_url1?toto", caption="my first photo"),
        _in_photos(caption="my second photo"),
        _in_photos(large="my_url3", caption="my third photo"),
        _in_photos(large="my_url4"),
    ]
}
expected_photos = [
    _out_photos(url="my_url1", caption="my first photo"),
    _out_photos(caption="my second photo"),
    _out_photos(url="my_url3", caption="my third photo"),
    _out_photos(url="my_url4"),
]


def _in_areas(areas=None):
    return areas if areas else []


def _in_area(**kwargs):
    return kwargs


def _out_area(name, equipments):
    return {
        "name": name,
        "equipments": equipments
    }


nominal_areas = _in_areas([_in_area(title="my_title", amenity_ids=[1, 2, 3])])
expected_areas = [_out_area(name="my_title", equipments=["1", "2", "3"])]


def _in_equipments(equipments=None):
    return equipments if equipments else []


def _in_equipment(**kwargs):
    return kwargs


def _out_equipment(name, description):
    return {
        "name": name,
        "description": description,
    }


nominal_equipments = _in_equipments([
    _in_equipment(id=1, name="eq1", description="desc1"),
    _in_equipment(id=2, name="eq2", description="desc2"),
    _in_equipment(id=3, name="eq3", description="desc3"),
])
expected_equipments = {
    "1": _out_equipment(name="eq1", description="desc1"),
    "2": _out_equipment(name="eq2", description="desc2"),
    "3": _out_equipment(name="eq3", description="desc3"),
}


def _in_eq_per_areas(areas, equipments):
    return {
        "see_all_amenity_sections": areas,
        "listing_amenities": equipments,
    }


def _out_eq_per_areas(areas, equipments):
    return {
        "areas": areas,
        "equipments": equipments
    }


def _in_price(**kwargs):
    return kwargs


def _out_price(label, value):
    return {
        "label": label,
        "value": value,
    }


nominal_prices = {
    "price_details": [
        _in_price(label="price1", value="1.5"),
        _in_price(label="price2", value="2.6"),
        _in_price(label="price3", value="3.7"),
    ]
}

expected_prices = [
    _out_price(label="price1", value="1.5"),
    _out_price(label="price2", value="2.6"),
    _out_price(label="price3", value="3.7"),
]


def _in_highlight(**kwargs):
    return kwargs


def _out_highlight(headline, message):
    return {
        "headline": headline,
        "message": message,
    }


nominal_highlights = {
    "highlights": [
        _in_highlight(headline="h1", message="m1"),
        _in_highlight(headline="h2", message="m2"),
        _in_highlight(headline="h3", message="m3"),
    ]
}
expected_highlights = [
    _out_highlight(headline="h1", message="m1"),
    _out_highlight(headline="h2", message="m2"),
    _out_highlight(headline="h3", message="m3"),
]


def _in_room(**kwargs):
    return kwargs


def _out_room(name, details):
    return {
        "name": name,
        "details": details,
    }


nominal_rooms = {
    "hometour_rooms": [
        _in_room(name_with_type="n1", highlights_hometour="d1"),
        _in_room(name_with_type="n2", highlights_hometour="d2"),
        _in_room(name_with_type="n3", highlights_hometour="d3"),
    ]
}
expected_rooms = [
    _out_room(name="n1", details="d1"),
    _out_room(name="n2", details="d2"),
    _out_room(name="n3", details="d3"),
]

# ----------------------------------------------------
# test cases
# ----------------------------------------------------


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
        (
            _in_eq_per_areas(nominal_areas, nominal_equipments),
            _out_eq_per_areas(expected_areas, expected_equipments),
        )
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

    # @parameterized.expand([
    #     (None, None),
    #     ({}, None),
    # ])
    # def test_get_airbnb_reviews(self, input, expected):
    #     self.assertEqual(_get_airbnb_reviews(input), expected)
