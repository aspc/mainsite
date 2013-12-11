from django.contrib import admin
from aspc.events.models import Event, FacebookEventPage

def approve_all(modeladmin, request, queryset):
    queryset.update(status='approved')
approve_all.short_description = "Approve selected events"

def deny_all(modeladmin, request, queryset):
    queryset.update(status='denied')
deny_all.short_description = "Deny selected events"

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'description']
    list_editable = ['status']
    ordering = ['status', 'name']
    actions = [approve_all, deny_all]

class FacebookEventPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    ordering = ['name']

admin.site.register(Event, EventAdmin)
admin.site.register(FacebookEventPage, FacebookEventPageAdmin)