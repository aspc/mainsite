from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from aspc.courses.models import (Section, Department, Meeting, Schedule,
    START_DATE, END_DATE)
from aspc.courses.forms import SearchForm, ICalExportForm
import re
import json
import datetime
import shlex
import subprocess
import vobject
from dateutil import rrule


def search(request):
    if request.method == "GET":
        if len(request.GET) > 0:
            form = SearchForm(request.GET)
            if form.is_valid():
                results_set = form.build_queryset()
                paginator = Paginator(results_set, per_page=20, orphans=10)
                GET_data = request.GET.copy()
                
                try:
                    page = int(request.GET.get('page', '1'))
                    if GET_data.get('page', False):
                        del GET_data['page']
                except ValueError:
                    page = 1
                
                try:
                    results = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    results = paginator.page(paginator.num_pages)
                
                return render(request, 'courses/search.html', {
                    'form': form,
                    'results': results,
                    'path': ''.join([request.path, '?', GET_data.urlencode()]),
                })
            else:
                return render(request, 'courses/search.html', {
                    'form': form,
                })
        else:
            form = SearchForm()
            return render(request, 'courses/search.html', {
                'form': form,
            })

def schedule(request):
    if not request.method == "GET" or len(request.GET) == 0:
        form = SearchForm()
        return render(request, 'courses/schedule.html', {
            'form': form,
        })
    else:
        form = SearchForm(request.GET)
        if form.is_valid():
            results_set = form.build_queryset()
            paginator = Paginator(results_set, per_page=10, orphans=5)
            GET_data = request.GET.copy()
            
            try:
                page = int(request.GET.get('page', '1'))
                if GET_data.get('page', False):
                    del GET_data['page']
            except ValueError:
                page = 1
            
            try:
                results = paginator.page(page)
            except (EmptyPage, InvalidPage):
                results = paginator.page(paginator.num_pages)
            
            for course in results.object_list:
                if course.id in request.session.get('schedule_courses', []):
                    course.added = True
            
            return render(request, 'courses/schedule.html', {
                'form': form,
                'results': results,
                'path': ''.join([request.path, '?', GET_data.urlencode()]),
            })
        else:
            return render(request, 'courses/schedule.html', {
                'form': form,
            })

def load_from_session(request):
    all_events = []
    valid_courses = set()
    schedule_courses = request.session.get('schedule_courses', set())
    for course in Section.objects.filter(id__in=schedule_courses):
        all_events.append(course.json())
        valid_courses.add(course.pk)
    if schedule_courses - valid_courses:
        for invalid in (schedule_courses - valid_courses):
            request.session['schedule_courses'].remove(invalid)
        request.session.modified = True
    return HttpResponse(content=json.dumps(all_events, cls=DjangoJSONEncoder), content_type='application/json')

def clear_schedule(request):
    courses_info = []
    if request.session.get('schedule_courses', False):
        schedule_courses = request.session['schedule_courses']
        del request.session['schedule_courses']
        for course in Section.objects.filter(id__in=schedule_courses):
            courses_info.append(course.json())
    return HttpResponse(content=json.dumps(courses_info, cls=DjangoJSONEncoder), content_type='application/json')

def share_schedule(request):
    schedule_courses = Section.objects.filter(id__in=request.session.get('schedule_courses',[]))
    if request.method == "POST":
        s = Schedule()
        s.save()
        for course in schedule_courses:
            s.sections.add(course)
        s.save()
        
        return render(request, 'courses/share_schedule.html', {'saved': True, 'schedule': s, 'schedule_courses': s.sections.all(),})
    else:
        return render(request, 'courses/share_schedule.html', {'schedule_courses': schedule_courses,})

def view_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    if request.method == "POST":
        request.session['schedule_courses'] = set([c.id for c in schedule.sections.all()])
        return HttpResponseRedirect(reverse('aspc.course.views.schedule'))
    else:
        return render(request, 'courses/schedule_frozen.html',{'schedule': schedule,})

def view_minimal_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    return render(request, 'courses/minimal_schedule_frozen.html', {'schedule': schedule,})

def ical_export(request, schedule_id=None):
    if schedule_id is not None:
        schedule = get_object_or_404(Schedule, pk=schedule_id)
        schedule_courses = schedule.sections.all()
    else:
        schedule_courses = Section.objects.filter(
            id__in=request.session.get('schedule_courses',[])
        )

    if request.method == "POST":
        form = ICalExportForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                'courses/ical_export.html',
                {'form': form, 'schedule_courses': schedule_courses}
            )

        icalendar = _ical_from_courses(
            schedule_courses,
            form.cleaned_data['start'],
            form.cleaned_data['end']
        )

        response = HttpResponse(icalendar.serialize(), content_type='text/calendar')

        if schedule_id is not None:
            filename = 'schedule_{0}.ics'.format(schedule_id)
        else:
            filename = 'schedule.ics'
        response['Filename'] = filename
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
    else:
        form = ICalExportForm(initial={
            'start': START_DATE,
            'end': END_DATE
        })
        return render(
            request,
            'courses/ical_export.html',
            {'form': form, 'schedule_courses': schedule_courses}
        )

def _ical_from_courses(courses, start_date, end_date):
    cal = vobject.iCalendar()
    cal.add('prodid').value = '-//Associated Students of Pomona College//Schedule Builder//EN'
    for course in courses:
        for meeting in course.meeting_set.all():
            v = cal.add('vevent')
            v.add('summary').value = '[{0}] {1}'.format(course.code, course.name)
            
            weekdays = []
            if meeting.monday: weekdays.append(rrule.MO)
            if meeting.tuesday: weekdays.append(rrule.TU)
            if meeting.wednesday: weekdays.append(rrule.WE)
            if meeting.thursday: weekdays.append(rrule.TH)
            if meeting.friday: weekdays.append(rrule.FR)
            
            timepairs = meeting.to_datetime_ranges(base_date=start_date)
            
            if not timepairs: # some meetings in CX don't have weekdays entered
                continue
            
            timepairs.sort()
            dtstart, dtend = timepairs[0]
            
            # Note: to_datetime_ranges is for the frontend. This is hacky, but
            # we want the actual first meeting, so we need to use START_DATE
            # as the base date for the timestamp.
            
            v.add('dtstart').value = dtstart
            v.add('dtend').value = dtend
            v.add('dtstamp').value = datetime.datetime.now()
            v.add('location').value = ', '.join((meeting.location, meeting.get_campus_display()))
            
            course_rr = rrule.rruleset()
            course_rr.rrule(rrule.rrule(
                rrule.WEEKLY,
                until=end_date,
                dtstart=dtstart,
                byweekday=weekdays
            ))
            
            v.rruleset = course_rr

    return cal

class CourseDetailView(generic.DetailView):
    model = Section
    slug_field = 'code_slug'
    slug_url_kwarg = 'course_code'
    def get_queryset(self):
        dept = get_object_or_404(Department, code=self.kwargs['dept'])
        return Section.objects.filter(course__primary_department=dept)


def schedule_course_add(request, course_code):
    course = get_object_or_404(Section, code_slug=course_code)
    if request.session.get('schedule_courses'):
        if not (course.id in request.session['schedule_courses']):
            request.session['schedule_courses'].add(course.id)
            request.session.modified = True
    else:
        request.session['schedule_courses'] = set([course.id,])
    return HttpResponse(content=json.dumps(course.json(), cls=DjangoJSONEncoder), content_type='application/json')


def schedule_course_remove(request, course_code):
    removed_ids = []
    course = get_object_or_404(Section, code_slug=course_code)
    if request.session.get('schedule_courses'):
        if (course.id in request.session['schedule_courses']):
            request.session['schedule_courses'].remove(course.id)
            request.session.modified = True
            
            course_data = course.json()
            for e in course_data['events']:
                removed_ids.append(e['id'])
    
    return HttpResponse(content=json.dumps(removed_ids, cls=DjangoJSONEncoder), content_type='application/json')

class DepartmentListView(generic.ListView):
    queryset = (Department.objects
                    .annotate(num_courses=Count('primary_course_set'))
                    .filter(num_courses__gt=0)
                    .distinct()
                    .order_by('code')
                )

class DepartmentCoursesView(generic.DetailView):
    model = Department
    slug_field = 'code'
