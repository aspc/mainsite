from django.conf.urls import *

from django.views.generic.base import TemplateView
from aspc.courses.views import SectionDetailView, DepartmentListView, DepartmentCoursesView, CourseDetailView
urlpatterns = [
    url(r'^schedule/$', 'aspc.courses.views.schedule', name="schedule"),
    url(r'^schedule/(?P<course_code>[\w\d-]+)/add/$', 'aspc.courses.views.schedule_course_add', name="course_add"),
    url(r'^schedule/(?P<course_code>[\w\d-]+)/remove/$', 'aspc.courses.views.schedule_course_remove', name="course_remove"),
    url(r'^schedule/(?P<schedule_id>\d+)/$', 'aspc.courses.views.view_schedule', name="view_schedule"),
    url(r'^schedule/(?P<schedule_id>\d+)/icalendar/$', 'aspc.courses.views.ical_export'),
    url(r'^schedule/icalendar/$', 'aspc.courses.views.ical_export'),
    url(r'^schedule/load/$', 'aspc.courses.views.load_from_session'),
    url(r'^schedule/clear/$', 'aspc.courses.views.clear_schedule'),
    url(r'^schedule/save/$', 'aspc.courses.views.share_schedule'),

    # TODO: Remove below with new courses app
    url(r'^search/$', 'aspc.courses.views.search'),
    url(r'^browse/$', DepartmentListView.as_view(), name="department_list"),
    url(r'^browse/(?P<slug>[A-Z]+)/$', DepartmentCoursesView.as_view(), name="department_detail"),
    url(r'^browse/course/(?P<course_code>[\w\d-]+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^browse/instructor/(?P<instructor>[\w\d-]+)/course/(?P<course_code>[\w\d-]+)/$', SectionDetailView.as_view(), name="section_detail"),
    url(r'^$', TemplateView.as_view(template_name='courses/landing.html'), name="courses_home"),
]