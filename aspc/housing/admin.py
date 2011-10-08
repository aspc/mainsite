from django.contrib import admin
from aspc.housing.models import Room, Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['room', 'create_ts',]
    exclude = ('room',)

class RoomAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'floor', 'size', 'occupancy', 'reserved', 'suite']
    ordering = ['floor']

admin.site.register(Room, RoomAdmin)
admin.site.register(Review, ReviewAdmin)
