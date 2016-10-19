from django import forms
from django.forms import Form
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Avg, Q
from django.views.generic import View, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from aspc.courses.models import (Section, Department, Schedule, RefreshHistory, START_DATE, END_DATE, Term, Course,
                                 Instructor, CourseReview, FeaturingQuery)
from aspc.courses.forms import SearchForm, ICalExportForm, ReviewSearchForm, ReviewForm
import json
import datetime
import vobject
import operator
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

def schedule(request):
    last_full, last_reg = _get_refresh_history()
    featuring_queries = FeaturingQuery.objects.all()

    if not request.method == "GET" or len(request.GET) == 0:
        form = SearchForm()
        return render(request, 'schedule/schedule.html', {
            'form': form,
            'last_full': last_full,
            'last_reg': last_reg,
            'featuring_queries': featuring_queries
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
                'last_reg': last_reg,
                'featuring_queries': featuring_queries
            })
        else:
            return render(request, 'schedule/schedule.html', {
                'form': form,
                'last_full': last_full,
                'last_reg': last_reg,
                'featuring_queries': featuring_queries
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
        if request.user.is_authenticated():
            s.user = request.user
        s.save()
        for course in schedule_courses:
            s.sections.add(course)

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

def my_schedules(request):
    schedules = request.user.schedule_set.order_by('-create_ts')
    return render(request, 'schedule/my_schedules.html', {'schedules': schedules})

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
            return Section.objects.filter(instructors__id__exact=self.kwargs['instructor_id'], course__code_slug=self.kwargs['course_code']).order_by('term','code_slug').first()
        except IndexError:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(SectionDetailView, self).get_context_data(**kwargs)
        instructor_object = Instructor.objects.get(id=self.kwargs['instructor_id'])
        course_object = Course.objects.get(code_slug=self.kwargs['course_code'])

        context['is_section'] = True
        context['professor'] = instructor_object
        context['current_term'] = Term.objects.all()[0]
        context['reviews'] = CourseReview.objects.filter(course=course_object, instructor=instructor_object).order_by('-created_date')
        context['miscellaneous_ratings'] = self.get_object().get_miscellaneous_ratings()

        return context

class CourseDetailView(generic.DetailView):
    model = Section
    slug_field = 'code_slug'
    slug_url_kwarg = 'course_code'
    template_name = "browse/course_detail.html"

    def get_object(self):
        try:
            # It doesn't really matter which Section object we return if there are multiple that fit the
            # <Course> identifier, but we ought to return the most recent one so the section data
            # that we display is as up-to-date as possible
            course = Course.objects.get(code_slug=self.kwargs['course_code'])
            return course.get_most_recent_section()
        except IndexError:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        course_object = Course.objects.get(code_slug=self.kwargs['course_code'])
        course_instructor_list = course_object.get_instructors_from_all_sections()
        course_instructor_list = list(set(course_instructor_list)) # Remove duplicates

        context['reviews'] = CourseReview.objects.filter(course=course_object).order_by('-created_date')
        context['average_rating'] = course_object.rating
        context['course_instructor_list'] = course_instructor_list
        context['miscellaneous_ratings'] = course_object.get_miscellaneous_ratings()
        return context

class InstructorDetailView(generic.DetailView):
	model = Instructor
	template_name = 'browse/instructor_detail.html'

	def get_object(self):
		try:
			return Instructor.objects.get(id=self.kwargs['instructor_id'])
		except IndexError:
			raise Http404

	def get_context_data(self, **kwargs):
		context = super(InstructorDetailView, self).get_context_data(**kwargs)

		instructor_object = Instructor.objects.get(id=self.kwargs['instructor_id'])
		sections_taught = Section.objects.filter(instructors=instructor_object)
		courses_taught = []
		for s in sections_taught:
			courses_taught.append(s.course)

		context['courses_taught'] = list(set(courses_taught))
		context['reviews'] = CourseReview.objects.filter(course__in=context['courses_taught'], instructor=instructor_object).order_by('-created_date')

		return context

class ReviewView(View):
    @method_decorator(login_required)
    def get(self, request, course_code, instructor_id=None):
        if instructor_id:
          course = Course.objects.get(code_slug=course_code)
          instructor = Instructor.objects.get(id=instructor_id)
          review = CourseReview.objects.get(author=request.user, course=course, instructor=instructor)
          form = ReviewForm(course_code, review)
        else:
          form = ReviewForm(course_code)
        return render(request, 'reviews/review_new.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request, course_code, instructor_id=None):
        form = ReviewForm(course_code, None, request.POST)
        if form.is_valid():
            instructor = form.cleaned_data["professor"]
            overall_rating = form.cleaned_data["overall_rating"]
            work_per_week = form.cleaned_data["work_per_week"]
            comments = form.cleaned_data["comments"]

            useful_rating = form.cleaned_data["useful_rating"]
            engagement_rating = form.cleaned_data["engagement_rating"]
            difficulty_rating = form.cleaned_data["difficulty_rating"]
            competency_rating = form.cleaned_data["competency_rating"]
            lecturing_rating = form.cleaned_data["lecturing_rating"]
            approachable_rating = form.cleaned_data["approachable_rating"]
            enthusiasm_rating = form.cleaned_data["enthusiasm_rating"]
            grade = form.cleaned_data["grade"]

            review, created = CourseReview.objects.get_or_create(author=request.user, course=form.course, instructor=instructor)
            review.overall_rating = int(overall_rating)
            review.work_per_week = work_per_week

            review.useful_rating = int(useful_rating)
            review.engagement_rating = int(engagement_rating)
            review.difficulty_rating = int(difficulty_rating)
            review.competency_rating = int(competency_rating)
            review.lecturing_rating = int(lecturing_rating)
            review.approachable_rating = int(approachable_rating)
            review.enthusiasm_rating = int(enthusiasm_rating)
            review.grade = int(grade) if grade else None
            review.comments = comments
            review.save()
            return redirect(reverse('section_detail', kwargs={"instructor_id": instructor.id, "course_code": course_code}))
        else:
            return render(request, 'reviews/review_new.html', {'form': form})


class ReviewSearchView(View):
    def get(self, request):
        form = ReviewSearchForm(request.GET)
        if len(request.GET) > 0:
            if form.is_valid():
                results_set, search_type = form.build_queryset()
                paginator = Paginator(results_set, per_page=20, orphans=10)
                GET_data = request.GET.copy()

                page = int(request.GET.get('page', '1'))
                GET_data.pop('page', None)

                try:
                    results = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    results = paginator.page(paginator.num_pages)

                return render(request, 'reviews/review_search.html', {
                    'form': form,
                    'did_perform_search': True,
                    'results': results,
                    'search_type': search_type,
                    'path': ''.join([request.path, '?', GET_data.urlencode()]),
                })
            else:
                return render(request, 'reviews/review_search.html', {
                    'form': form,
                })
        else:
            return render(request, 'reviews/review_search.html', {
                'form': form,
            })

def featuring_query(request, name):
    # query = Query.objects.get(name=name)
    # section = query.get_instance()
    section = Section.objects.all()[4747];
    return render(request, 'schedule/search/search_result.html', {'c':section})
