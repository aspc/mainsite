from django.contrib import admin
from aspc.senate.models import Position, Appointment, Document

class PositionAdmin(admin.ModelAdmin):
    list_display = ("title",  "description", "sort_order",)

class DocumentAdmin(admin.ModelAdmin):
    def public_url(self, obj):
        return obj.file.url
    public_url.short_description = "Public URL"
    
    raw_id_fields = ('uploaded_by',)
    list_display = ("title", "uploaded_by", "uploaded_at", "public_url",)
    
    related_lookup_fields = {
        'fk': ['uploaded_by',],
    }

admin.site.register(Position, PositionAdmin)
admin.site.register(Appointment)
admin.site.register(Document, DocumentAdmin)
