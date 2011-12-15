from django.contrib import admin
from django.db import models
from aspc.minutes.models import MeetingMinutes

class MeetingMinutesAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ['date', 'summary']

admin.site.register(MeetingMinutes, MeetingMinutesAdmin)