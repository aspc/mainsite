from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from aspc.senate.models import Position, Appointment, Document

class PositionAdmin(admin.ModelAdmin):
    list_display = ("title",  "description", "sort_order",)

class AppointmentAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("position",  "name", "login_id", "start", "end")
    exclude = ("user",)

class DocumentAdmin(admin.ModelAdmin):
    def public_url(self, obj):
        return obj.file.url
    public_url.short_description = "Public URL"
    
    list_display = ("title", "uploaded_by", "uploaded_at", "public_url",)
    exclude = ("uploaded_by",)
    
    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        obj.save()

admin.site.register(Position, PositionAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Document, DocumentAdmin)
