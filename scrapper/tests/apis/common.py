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


def _out_general_info(bathroom=0, bed=0, bedroom=0, guest=0):
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

input_equipments_per_areas = _in_eq_per_areas(nominal_areas, nominal_equipments)
expected_equipments_per_areas = _out_eq_per_areas(expected_areas, expected_equipments)

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

nominal_review = {
    "author": {
        "has_profile_pic": True,
        "first_name": "toto",
        "picture_url": "https://toto.fr"
    },
    "comments": "a comment",
    "created_at": "2008-02-03T10-09",
    "language": "fr",
    "rating": 5,
}
expected_review = {
    "author_name": "toto",
    "author_picture_url": "https://toto.fr",
    "review": "a comment",
    "date": "2008-02-03",
    "language": "fr",
}

full_input_details = {
    "pdp_listing_detail": {
        "p3_summary_title": "a name",
        "sectioned_description": {
            "description": "a description"
        },
        "guest_controls": {
            "structured_house_rules": ["rule 1", "rule 2"]
        }
    },
}

full_input_reviews = {
    "reviews": [nominal_review]
}

full_input_details["pdp_listing_detail"] |= nominal_host_info
full_input_details["pdp_listing_detail"] |= nominal_general_info
full_input_details["pdp_listing_detail"] |= nominal_location
full_input_details["pdp_listing_detail"] |= nominal_photos
full_input_details["pdp_listing_detail"] |= input_equipments_per_areas
full_input_details["pdp_listing_detail"] |= nominal_prices
full_input_details["pdp_listing_detail"] |= nominal_highlights
full_input_details["pdp_listing_detail"] |= nominal_rooms

full_converted_data = {
    "name": "a name",
    "general_info": expected_general_info,
    "host": expected_nominal_host_info,
    "location": expected_location,
    "photos": expected_photos,
    "description": ["a description"],
    "equipments": expected_equipments_per_areas,
    "reviews": [expected_review],
    "prices": expected_prices,
    "highlights": expected_highlights,
    "house_rules": ["rule 1", "rule 2"],
    "rooms": expected_rooms,
}
