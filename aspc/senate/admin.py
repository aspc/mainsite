from django.contrib import admin
from aspc.senate.models import Position, Appointment

class PositionAdmin(admin.ModelAdmin):
    list_display = ("title",  "description", "sort_order",)

admin.site.register(Position, PositionAdmin)
admin.site.register(Appointment)
