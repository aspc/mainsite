from django.contrib import admin
from aspc.college.models import Term, Building, Floor

class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'shortname', 'type', 'latitude', 'longitude']

class FloorAdmin(admin.ModelAdmin):
    list_display = ['building_name', 'number']

admin.site.register(Term)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Floor, FloorAdmin)