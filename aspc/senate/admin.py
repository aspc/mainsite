from django.contrib import admin
from aspc.senate.models import Position, Appointment, Document

class PositionAdmin(admin.ModelAdmin):
    list_display = ("title",  "description", "sort_order",)

class DocumentAdmin(admin.ModelAdmin):
    def public_url(self, obj):
        return obj.file.url
    public_url.short_description = "Public URL"
    list_display = ("title", "uploaded_by", "uploaded_at", "public_url",)

admin.site.register(Position, PositionAdmin)
admin.site.register(Appointment)
admin.site.register(Document, DocumentAdmin)
