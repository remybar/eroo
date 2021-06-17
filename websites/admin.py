from django.contrib import admin

from .models import (
    Website,
    WebsiteHost,
    WebsitePhoto,
    WebsiteLocation,
    Room,
    RoomDetail,
    Testimonial,
    Equipment,
    EquipmentArea,
    Highlight,
    Rule,
)

admin.site.register(Website)
admin.site.register(WebsiteHost)
admin.site.register(WebsitePhoto)
admin.site.register(WebsiteLocation)
admin.site.register(Room)
admin.site.register(RoomDetail)
admin.site.register(Testimonial)
admin.site.register(Equipment)
admin.site.register(EquipmentArea)
admin.site.register(Highlight)
admin.site.register(Rule)
