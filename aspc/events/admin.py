from django.contrib import admin
from aspc.events.models import Event, FacebookEventPage

def approve_all(modeladmin, request, queryset):
    queryset.update(status='approved')
approve_all.short_description = "Approve selected events"

def deny_all(modeladmin, request, queryset):
    queryset.update(status='denied')
deny_all.short_description = "Deny selected events"

class EventAdmin(admin.ModelAdmin):
    list_display = ('get_status_display_colored', 'name', 'start', 'get_description_display')
    list_display_links = ('name',)
    list_filter = ('status',)
    ordering = ('-status', '-start', 'end', 'name')
    list_per_page = 50
    actions = (approve_all, deny_all)

class FacebookEventPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'page_id', 'url')
    ordering = ('name',)

admin.site.register(Event, EventAdmin)
admin.site.register(FacebookEventPage, FacebookEventPageAdmin)