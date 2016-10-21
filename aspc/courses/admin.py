from django.contrib import admin
from aspc.courses.models import (Section, Course, Department, Meeting, RequirementArea, RefreshHistory, CourseReview,
								 FeaturingQuery)

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'course_count')

class MeetingAdmin(admin.ModelAdmin):
	list_display = ('section', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'begin', 'end', 'location',)

class MeetingInline(admin.TabularInline):
	model = Meeting
	list_display = ('section', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'begin', 'end', 'location',)

class CourseAdmin(admin.ModelAdmin):
	list_display = ('code', 'number', 'name',  'primary_department')

class SectionAdmin(admin.ModelAdmin):
	list_display = ('code', 'course', 'term', 'description', 'credit', 'spots', 'filled', 'perms')
	inlines = [MeetingInline]

class CourseReviewAdmin(admin.ModelAdmin):
	list_display = ('author', 'course', 'instructor', 'overall_rating')

admin.site.register(Course, CourseAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(RequirementArea, DepartmentAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(CourseReview, CourseReviewAdmin)
admin.site.register(RefreshHistory)
admin.site.register(FeaturingQuery)