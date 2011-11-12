from django.contrib import admin
from aspc.coursesearch.models import Course, Department, Meeting

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'course_count')

class MeetingAdmin(admin.ModelAdmin):
    list_display = ('course', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'begin', 'end', 'location',)

class MeetingInline(admin.TabularInline):
    model = Meeting
    #list_display = ('course', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'begin', 'end', 'location',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'instructor',)
    inlines = [MeetingInline,]

admin.site.register(Course, CourseAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Meeting, MeetingAdmin)