from django.contrib import admin
from django.db import models
from aspc.minutes.models import MeetingMinutes
from aspc.widgets import MarkdownTextarea

class MeetingMinutesAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'

admin.site.register(MeetingMinutes, MeetingMinutesAdmin)