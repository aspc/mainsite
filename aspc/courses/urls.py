from django.conf.urls import *
from django.views.generic.base import TemplateView
from aspc.courses.views import SectionDetailView, CourseDetailView, InstructorDetailView, ReviewView, ReviewSearchView

urlpatterns = [
	# Home: /courses
    url(r'^$', TemplateView.as_view(template_name='courses/home.html'), name="courses_home"),

	# Planner: /courses/schedule
    url(r'^schedule/$', 'aspc.courses.views.schedule', name="course_planner"),
    url(r'^schedule/(?P<section_code_slug>[\w\d-]+)/add/$', 'aspc.courses.views.schedule_course_add', name="course_add"),
    url(r'^schedule/(?P<section_code_slug>[\w\d-]+)/remove/$', 'aspc.courses.views.schedule_course_remove', name="course_remove"),
    url(r'^schedule/(?P<schedule_id>\d+)/$', 'aspc.courses.views.view_schedule', name="view_schedule"),
    url(r'^schedule/(?P<schedule_id>\d+)/icalendar/$', 'aspc.courses.views.ical_export'),
    url(r'^schedule/icalendar/$', 'aspc.courses.views.ical_export'),
    url(r'^schedule/load/$', 'aspc.courses.views.load_from_session'),
    url(r'^schedule/clear/$', 'aspc.courses.views.clear_schedule'),
    url(r'^schedule/save/$', 'aspc.courses.views.share_schedule'),
    url(r'^schedule/my_schedules/$', 'aspc.courses.views.my_schedules', name='my_schedules'),
    url(r'^schedule/query/(?P<name>\w+)/$', 'aspc.courses.views.featuring_query', name="featuring_query"),

	# Browse: /courses/browse
	url(r'^browse/course/(?P<course_code>[\w\d-]+)/$', CourseDetailView.as_view(), name="course_detail"),
	url(r'^browse/instructor/(?P<instructor_id>[\d-]+)/$', InstructorDetailView.as_view(), name="instructor_detail"),
	url(r'^browse/instructor/(?P<instructor_id>\d+)/course/(?P<course_code>[\w\d-]+)/$', SectionDetailView.as_view(), name="section_detail"),

	# Reviews: /courses/reviews
	url(r'^reviews/$', ReviewSearchView.as_view(), name="search_reviews"),
    url(r'^reviews/unsubscribe/$', 'aspc.courses.views.unsubscribe', name="unsubscribe"),
	url(r'^reviews/(?P<course_code>[\w\d-]+)/$', ReviewView.as_view(), name="write_review"),
	url(r'^reviews/(?P<course_code>[\w\d-]+)/instructor/(?P<instructor_id>\d+)$', ReviewView.as_view(), name="write_review"),
]
