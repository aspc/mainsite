from django.conf.urls import *

from django.views.generic.base import TemplateView
from aspc.coursesearch.views import CourseDetailView, DepartmentListView, DepartmentCoursesView
from aspc.coursesearch.models import Department, Course

urlpatterns = [
    (r'^search/$', 'aspc.coursesearch.views.search'),
    (r'^schedule/$', 'aspc.coursesearch.views.schedule'),
    url(r'^schedule/(?P<course_code>[\w\d-]+)/add/$', 'aspc.coursesearch.views.schedule_course_add', name="course_add"),
    url(r'^schedule/(?P<course_code>[\w\d-]+)/remove/$', 'aspc.coursesearch.views.schedule_course_remove', name="course_remove"),
    (r'^schedule/(?P<schedule_id>\d+)/$', 'aspc.coursesearch.views.view_schedule'),
    (r'^schedule/(?P<schedule_id>\d+)/minimal/$', 'aspc.coursesearch.views.view_minimal_schedule'),
    (r'^schedule/(?P<schedule_id>\d+)/icalendar/$', 'aspc.coursesearch.views.ical_export'),
    (r'^schedule/icalendar/$', 'aspc.coursesearch.views.ical_export'),
    (r'^schedule/load/$', 'aspc.coursesearch.views.load_from_session'),
    (r'^schedule/clear/$', 'aspc.coursesearch.views.clear_schedule'),
    (r'^schedule/save/$', 'aspc.coursesearch.views.share_schedule'),
    url(r'^browse/$', DepartmentListView.as_view(), name="department_list"),
    url(r'^browse/(?P<slug>[A-Z]+)/$', DepartmentCoursesView.as_view(), name="department_detail"),
    url(r'^browse/(?P<dept>[A-Z]+)/(?P<course_code>[\w\d-]+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^$', TemplateView.as_view(template_name='coursesearch/landing.html'), name="coursesearch_home"),
]