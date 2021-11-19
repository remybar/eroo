from django.contrib import admin

from .models import (
    Website,
    WebsiteHost,
    WebsitePhoto,
    WebsiteLocation,
    Room,
    RoomDetail,
    Review,
    Equipment,
    EquipmentArea,
    Highlight,
    Rule,
)


class WebsiteAdmin(admin.ModelAdmin):
    readonly_fields = ('generated_date',)
    list_display = ('user', 'name', 'key', 'generated_date')


admin.site.register(Website, WebsiteAdmin)
admin.site.register(WebsiteHost)
admin.site.register(WebsitePhoto)
admin.site.register(WebsiteLocation)
admin.site.register(Room)
admin.site.register(RoomDetail)
admin.site.register(Review)
admin.site.register(Equipment)
admin.site.register(EquipmentArea)
admin.site.register(Highlight)
admin.site.register(Rule)
