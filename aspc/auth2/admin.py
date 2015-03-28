from django.contrib import admin
from aspc.auth2.models import UserData

class UserDataAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'college', 'year', 'dorm')

admin.site.register(UserData, UserDataAdmin)