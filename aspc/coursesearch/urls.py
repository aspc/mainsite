from django.conf.urls import *

from django.views.generic import list_detail
from aspc.coursesearch.models import Department, Course
from django.db.models import Count

urlpatterns = patterns('',
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
    url(r'^browse/$', list_detail.object_list, {'queryset': Department.objects.annotate(num_courses=Count('primary_course_set')).filter(num_courses__gt=0).distinct().order_by('code'),}, name="department_list"),
    url(r'^browse/(?P<slug>[A-Z]+)/$', list_detail.object_detail, {'queryset': Department.objects.all(), 'slug_field': 'code',}, name="department_detail"),
    url(r'^browse/(?P<dept>[A-Z]+)/(?P<course_code>[\w\d-]+)/$', 'aspc.coursesearch.views.course_detail', name="course_detail"),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'coursesearch/landing.html',}, name="coursesearch_home"),
)
