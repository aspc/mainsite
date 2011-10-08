from django.contrib import admin
from aspc.college.models import Term, Building, Floor, Map

class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'shortname', 'type', 'latitude', 'longitude']

class FloorAdmin(admin.ModelAdmin):
    list_display = ['building_name', 'number']

class MapAdmin(admin.ModelAdmin):
    list_display = ['get_building', 'floor', 'n', 'e', 's', 'w']

admin.site.register(Term)
admin.site.register(Map, MapAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Floor, FloorAdmin)
