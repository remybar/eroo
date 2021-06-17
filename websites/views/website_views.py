from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from ..models import (
    Website,
    WebsiteHost,
    WebsitePhoto,
    Testimonial,
    Highlight,
    EquipmentArea,
    RoomDetail,
    Room,
    Rule,
)
from ..config import (
    HOST_PICTURE_FILENAME,
)
from ..utils import partition_list

EQUIPMENT_COLUMN_COUNT = 4


def _build_context(website):
    return {
        "key": website.key,
        "name": website.name,
        "hostname": WebsiteHost.objects.filter(website=website).first().name,
    }


class WebsiteHomePage(LoginRequiredMixin, DetailView):
    template_name = "websites/template1/pages/home.html"
    model = Website
    slug_field = "key"
    slug_url_kwarg = "key"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object:
            website = self.object
            context |= _build_context(website)
            context |= {
                "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
                "description": website.description,
                "main_photo": WebsitePhoto.objects.filter(website=website).first().filename,
                "general_info": {
                    "bathroom_count": website.bathroom_count,
                    "bed_count": website.bed_count,
                    "bedroom_count": website.bedroom_count,
                    "guest_count": website.guest_count,
                },
                "location": {
                    "title": website.location.title,
                    "latitude": website.location.latitude,
                    "longitude": website.location.longitude,
                },
                "testimonials": [
                    {
                        "author_name": t.author_name,
                        "author_picture_filename": t.author_picture_filename,
                        "review": t.review,
                        "date": t.date,
                        "language": t.language,
                    }
                    for t in Testimonial.objects.filter(website=website)
                ],
                "highlights": [
                    {
                        "title": h.title,
                        "message": h.message,
                    }
                    for h in Highlight.objects.filter(website=website)
                ],
            }
        return context


class WebsitePhotosPage(LoginRequiredMixin, DetailView):
    template_name = "websites/template1/pages/photos.html"
    model = Website
    slug_field = "key"
    slug_url_kwarg = "key"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object:
            website = self.object
            context |= _build_context(website)
            context |= {
                "photos": [
                    {"filename": photo.filename, "caption": photo.caption}
                    for photo in WebsitePhoto.objects.filter(website=website)
                ],
            }
        return context


class WebsiteDetailsPage(LoginRequiredMixin, DetailView):
    template_name = "websites/template1/pages/details.html"
    model = Website
    slug_field = "key"
    slug_url_kwarg = "key"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object:
            website = self.object
            context |= _build_context(website)
            context |= {
                "equipments_per_area": [
                    {
                        "name": a.name,
                        "equipments": partition_list(
                            [
                                {
                                    "name": e.name,
                                    "description": e.description,
                                }
                                for e in a.equipments.all()
                            ],
                            EQUIPMENT_COLUMN_COUNT,
                        ),
                    }
                    for a in EquipmentArea.objects.filter(website=website)
                ],
                "rules": [r.name for r in Rule.objects.filter(website=website)],
                "rooms": [
                    {
                        "name": r.name,
                        "details": " · ".join(
                            [d.detail for d in RoomDetail.objects.filter(room=r)]
                        ),
                    }
                    for r in Room.objects.filter(website=website)
                ],
            }
        return context


class WebsiteContactPage(LoginRequiredMixin, DetailView):
    template_name = "websites/template1/pages/contact.html"
    model = Website
    slug_field = "key"
    slug_url_kwarg = "key"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object:
            website = self.object
            host = WebsiteHost.objects.filter(website=website).first()
            context |= _build_context(website)
            context |= {
                "host": {
                    "name": host.name,
                    "picture": HOST_PICTURE_FILENAME,
                    "description": host.description,
                    "languages": host.languages.replace(",", " · "),
                }
            }
        return context
