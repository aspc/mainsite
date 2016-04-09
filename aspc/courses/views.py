from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from aspc.courses.models import (Section, Department, Schedule, RefreshHistory, START_DATE, END_DATE, Term, Course, Instructor)
from aspc.courses.forms import SearchForm, ICalExportForm
import json
import datetime
import vobject
from dateutil import rrule

def _get_refresh_history():
    try:
        last_full = RefreshHistory.objects.order_by(
            '-last_refresh_date'
        ).filter(
            type=RefreshHistory.FULL
        )[0]
    except IndexError:
        last_full = None

    try:
        last_reg = RefreshHistory.objects.order_by(
            '-last_refresh_date'
        ).filter(
            type=RefreshHistory.REGISTRATION
        )[0]
    except IndexError:
        last_reg = None

    return last_full, last_reg

def search(request):
    last_full, last_reg = _get_refresh_history()

    if request.method == "GET":
        if len(request.GET) > 0:
            form = SearchForm(request.GET)
            if form.is_valid():
                results_set, term = form.build_queryset_and_term()
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

                return render(request, 'search/search.html', {
                    'form': form,
                    'results': results,
                    'path': ''.join([request.path, '?', GET_data.urlencode()]),
                    'last_full': last_full,
                    'last_reg': last_reg
                })
            else:
                return render(request, 'search/search.html', {
                    'form': form,
                    'last_full': last_full,
                    'last_reg': last_reg
                })
        else:
            form = SearchForm()
            return render(request, 'search/search.html', {
                'form': form,
                'last_full': last_full,
                'last_reg': last_reg
            })
    else:
        return HttpResponseNotAllowed(['GET'])

def schedule(request):
    last_full, last_reg = _get_refresh_history()

    if not request.method == "GET" or len(request.GET) == 0:
        form = SearchForm()
        return render(request, 'schedule/schedule.html', {
            'form': form,
            'last_full': last_full,
            'last_reg': last_reg
        })
    else:
        form = SearchForm(request.GET)
        if form.is_valid():
            results_set, term = form.build_queryset_and_term()
            request.session['term_key'] = term.key
            paginator = Paginator(results_set, per_page=20, orphans=5)
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

            return render(request, 'schedule/schedule.html', {
                'form': form,
                'results': results,
                'path': ''.join([request.path, '?', GET_data.urlencode()]),
                'last_full': last_full,
                'last_reg': last_reg
            })
        else:
            return render(request, 'schedule/schedule.html', {
                'form': form,
                'last_full': last_full,
                'last_reg': last_reg
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

        return render(request, 'schedule/schedule_share.html', {'saved': True, 'schedule': s, 'schedule_courses': s.sections.all(),})
    else:
        return render(request, 'schedule/schedule_share.html', {'schedule_courses': schedule_courses,})

def view_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    if request.method == "POST":
        request.session['schedule_courses'] = set([c.id for c in schedule.sections.all()])
        return HttpResponseRedirect(reverse('aspc.courses.views.schedule'))
    else:
        return render(request, 'schedule/schedule_frozen.html',{'schedule': schedule,})

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
                'schedule/schedule_ical_export.html',
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
            'schedule/schedule_ical_export.html',
            {'form': form, 'schedule_courses': schedule_courses}
        )

def _ical_from_courses(courses, start_date, end_date):
    cal = vobject.iCalendar()
    cal.add('prodid').value = '-//Associated Students of Pomona College//Schedule Builder//EN'
    for course in courses:
        for meeting in course.meeting_set.all():
            v = cal.add('vevent')
            v.add('summary').value = '[{0}] {1}'.format(course.code, course.course.name)

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

def schedule_course_add(request, section_code_slug):
    section = _get_section_for_term(section_code_slug=section_code_slug, term_key=request.session.get('term_key'))
    if request.session.get('schedule_courses'):
        if not (section.id in request.session['schedule_courses']):
            request.session['schedule_courses'].add(section.id)
            request.session.modified = True
    else:
        request.session['schedule_courses'] = set([section.id,])
    return HttpResponse(content=json.dumps(section.json(), cls=DjangoJSONEncoder), content_type='application/json')

def schedule_course_remove(request, section_code_slug):
    removed_ids = []
    section = _get_section_for_term(section_code_slug=section_code_slug, term_key=request.session.get('term_key'))
    if request.session.get('schedule_courses'):
        if (section.id in request.session['schedule_courses']):
            request.session['schedule_courses'].remove(section.id)
            request.session.modified = True

            section_data = section.json()
            for e in section_data['events']:
                removed_ids.append(e['id'])
    return HttpResponse(content=json.dumps(removed_ids, cls=DjangoJSONEncoder), content_type='application/json')

def _get_section_for_term(section_code_slug, term_key):
	all_sections = Section.objects.filter(code_slug=section_code_slug)

	try:
		section = all_sections.filter(term=Term.objects.get(key=term_key))[0] if term_key else all_sections[0]
	except IndexError:
		raise Http404

	return section

class SectionDetailView(generic.DetailView):
    model = Section
    slug_field = 'code_slug'
    slug_url_kwarg = 'course_code'
    template_name = "browse/section_detail.html"

    def get_object(self):
        try:
            # It doesn't really matter which Section object we return if there are multiple that fit the
            # <Instructor, Course> identifier, but we ought to return the most recent one so the section data
            # that we display is as up-to-date as possible
            return Section.objects.filter(instructors__id__exact=self.kwargs['instructor_id'], course__code_slug=self.kwargs['course_code']).order_by('term')[0]
        except IndexError:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(SectionDetailView, self).get_context_data(**kwargs)
        context['is_section'] = True
        context['professor'] = Instructor.objects.get(id=self.kwargs['instructor_id'])
        return context

class CourseDetailView(generic.DetailView):
    model = Section
    slug_field = 'code_slug'
    slug_url_kwarg = 'course_code'
    template_name = "browse/course_detail.html"

    def get_object(self):
        try:
            course = Course.objects.get(code_slug=self.kwargs['course_code'])
            return course.sections.all().order_by('term')[0]
        except IndexError:
            raise Http404
