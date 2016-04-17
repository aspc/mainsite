from django import forms
from aspc.courses.models import (Department, Section, Meeting, Term, Course, Instructor,
                                 RequirementArea, CAMPUSES, CAMPUSES_FULL_NAMES, CAMPUSES_LOOKUP)
from django.db.models import Count, F

import re
from itertools import groupby
from django.forms.widgets import Widget, Select
from django.forms.models import ModelChoiceIterator
from django.utils.safestring import mark_safe
from django.db.models import Q
import operator

def requirement_area_label(campus_value):
    return CAMPUSES_FULL_NAMES[campus_value]


class GroupedModelChoiceField(forms.ModelChoiceField):
    def __init__(self, group_by_field, group_label=None, *args, **kwargs):
        """
        group_by_field is the name of a field on the model
        group_label is a function to return a label for each choice group
        """
        super(GroupedModelChoiceField, self).__init__(*args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label

    def _get_choices(self):
        """
        Exactly as per ModelChoiceField except returns new iterator class
        """
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)

    choices = property(_get_choices, forms.ModelChoiceField._set_choices)

    def label_from_instance(self, obj):
        campus_code = CAMPUSES[obj.campus - 1][1]
        reqarea_name = re.sub(campus_code + r'\s+?', '', obj.name)
        return reqarea_name


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        else:
            for group, choices in groupby(self.queryset.all(),
                                          key=lambda row: getattr(row, self.field.group_by_field)):
                yield (self.field.group_label(group), [self.choice(ch) for ch in choices])


class DeptModelChoice(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.code, obj.name)


TIME_INPUT_FORMATS = [
    '%H:%M:%S',
    '%H:%M',
    '%I:%M%p',
    '%I:%M %p',
]

POSSIBLE_CREDIT = (
    ('A', 'any'), ('F', 'full'), ('P', 'partial'), (0.0, '0.0'), (0.25, '0.25'), (0.5, '0.5'), (1.0, '1.0'),
    (1.5, '1.5'),
    (2.0, '2.0'), (3.0, '3.0'), (4.0, '4.0'), (6.0, '6.0'))

keyword_regex = re.compile(r'(\w+)')


class SearchForm(forms.Form):
    term = forms.ModelChoiceField(
        queryset=Term.objects.annotate(num_sections=Count('sections')).filter(num_sections__gt=0), empty_label=None,
        required=True)
    department = DeptModelChoice(queryset=Department.objects.annotate(
        num_courses=Count('course_set')). \
        filter(num_courses__gt=0).distinct().order_by('code'),
                                 required=False, empty_label="(any)"
    )
    requirement_area = GroupedModelChoiceField(
        'campus',
        group_label=requirement_area_label,
        queryset=RequirementArea.objects.annotate(num_courses=Count('course_set')). \
            filter(num_courses__gt=0).distinct().order_by('code'),
        required=False, empty_label="(no particular)"
    )
    only_at_least = forms.ChoiceField(choices=(('A', 'at least'), ('O', 'only'),))
    m = forms.BooleanField(required=False)
    t = forms.BooleanField(required=False)
    w = forms.BooleanField(required=False)
    r = forms.BooleanField(required=False)
    f = forms.BooleanField(required=False)

    instructor = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'size': '40'}))
    # spots_left = forms.BooleanField(required=False, initial=True)
    course_number_min = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'size': '4'}))
    course_number_max = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'size': '4'}))
    credit = forms.ChoiceField(choices=POSSIBLE_CREDIT)

    start_range = forms.TimeField(required=False, input_formats=TIME_INPUT_FORMATS, widget=forms.TextInput(
        attrs={'size': '10'})) #widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    end_range = forms.TimeField(required=False, input_formats=TIME_INPUT_FORMATS, widget=forms.TextInput(
        attrs={'size': '10'})) #widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))

    c_cgu = forms.BooleanField(required=False)
    c_cm = forms.BooleanField(required=False)
    c_ks = forms.BooleanField(required=False)
    c_hm = forms.BooleanField(required=False)
    c_po = forms.BooleanField(required=False)
    c_pz = forms.BooleanField(required=False)
    c_sc = forms.BooleanField(required=False)

    keywords = forms.CharField(max_length=100, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        if self._errors:
            return cleaned_data # user has to fix field errors first
        if not any(map(cleaned_data.get, ('m', 't', 'w', 'r', 'f', 'instructor',
                                          'start_range', 'end_range', 'c_cgu', 'c_cm', 'c_ks', 'c_hm', 'c_po', 'c_pz',
                                          'c_sc',
                                          'department', 'requirement_area', 'keywords'))):
            raise forms.ValidationError("You must specify at least one constraint.")
        return cleaned_data

    def build_queryset_and_term(self):
        term = self.cleaned_data['term']
        qs = Section.objects.filter(term=term)
        if self.cleaned_data.get('department'):
            qs = qs.filter(course__departments=self.cleaned_data['department'])

        if self.cleaned_data.get('requirement_area'):
            qs = qs.filter(course__requirement_areas=self.cleaned_data['requirement_area'])

        if self.cleaned_data.get('only_at_least') == 'O':

            m = Meeting.objects.filter(monday=True)
            if self.cleaned_data.get('m', False):
                qs = qs.filter(meeting__in=m)
            else:
                qs = qs.exclude(meeting__in=m)

            t = Meeting.objects.filter(tuesday=True)
            if self.cleaned_data.get('t', False):
                qs = qs.filter(meeting__in=t)
            else:
                qs = qs.exclude(meeting__in=t)

            w = Meeting.objects.filter(wednesday=True)
            if self.cleaned_data.get('w', False):
                qs = qs.filter(meeting__in=w)
            else:
                qs = qs.exclude(meeting__in=w)

            r = Meeting.objects.filter(thursday=True)
            if self.cleaned_data.get('r', False):
                qs = qs.filter(meeting__in=r)
            else:
                qs = qs.exclude(meeting__in=r)

            f = Meeting.objects.filter(friday=True)
            if self.cleaned_data.get('f', False):
                qs = qs.filter(meeting__in=f)
            else:
                qs = qs.exclude(meeting__in=f)

            if self.cleaned_data.get('start_range'):
                qs = qs.filter(meeting__in=Meeting.objects.filter(begin__gte=self.cleaned_data['start_range']))
            if self.cleaned_data.get('end_range'):
                qs = qs.filter(meeting__in=Meeting.objects.filter(end__lte=self.cleaned_data['end_range']))

        elif self.cleaned_data.get('only_at_least') == 'A':
            if self.cleaned_data.get('m') == True: qs = qs.filter(meeting__monday=self.cleaned_data['m'])
            if self.cleaned_data.get('t') == True: qs = qs.filter(meeting__tuesday=self.cleaned_data['t'])
            if self.cleaned_data.get('w') == True: qs = qs.filter(meeting__wednesday=self.cleaned_data['w'])
            if self.cleaned_data.get('r') == True: qs = qs.filter(meeting__thursday=self.cleaned_data['r'])
            if self.cleaned_data.get('f') == True: qs = qs.filter(meeting__friday=self.cleaned_data['f'])
            if self.cleaned_data.get('start_range'):
                qs = qs.filter(meeting__begin__gte=self.cleaned_data['start_range'])
            if self.cleaned_data.get('end_range'):
                qs = qs.filter(meeting__end__lte=self.cleaned_data['end_range'])

        campus_ids = []
        if self.cleaned_data.get('c_cgu'): campus_ids.append(CAMPUSES_LOOKUP['CGU'])
        if self.cleaned_data.get('c_cm'): campus_ids.append(CAMPUSES_LOOKUP['CMC'])
        if self.cleaned_data.get('c_ks'): campus_ids.append(CAMPUSES_LOOKUP['KS'])
        if self.cleaned_data.get('c_hm'): campus_ids.append(CAMPUSES_LOOKUP['HM'])
        if self.cleaned_data.get('c_po'): campus_ids.append(CAMPUSES_LOOKUP['PO'])
        if self.cleaned_data.get('c_pz'): campus_ids.append(CAMPUSES_LOOKUP['PZ'])
        if self.cleaned_data.get('c_sc'): campus_ids.append(CAMPUSES_LOOKUP['SC'])

        if campus_ids:
            qs = qs.filter(meeting__campus__in=campus_ids)

        if self.cleaned_data.get('course_number_min'):
            qs = qs.filter(course__number__gte=self.cleaned_data.get('course_number_min'))

        if self.cleaned_data.get('course_number_max'):
            qs = qs.filter(course__number__lte=self.cleaned_data.get('course_number_max'))

        if self.cleaned_data.get('instructor'):
            # Split the instructor name into word tokens, use anything except hyphens as the delimiter
            # E.g.
            # "Hillary Rodham Clinton" -> ["Hillary", "Rodham", "Clinton"]
            # "Hillary Rodham-Clinton" -> ["Hillary", "Rodham-Clinton"]
            # "Clinton, Hillary Rodham" -> ["Clinton", "Hillary", "Rodham"]
            instructor_tokens = re.split('(?!-)\W+', self.cleaned_data['instructor'])

            # Progessively filter the instructor name field by each token
            # Possible performance impact but names should only be at most three tokens long, so only three iterations
            for t in instructor_tokens:
                qs = qs.filter(instructors__name__icontains=t)
        if self.cleaned_data.get('credit'):
            if self.cleaned_data['credit'] == 'A':
                pass
            elif self.cleaned_data['credit'] == 'F':
                qs = qs.filter(credit__gte=1.0)
            elif self.cleaned_data['credit'] == 'P':
                qs = qs.filter(credit__lt=1.0, credit__gt=0.0)
            else:
                qs = qs.filter(credit=self.cleaned_data['credit'])

        # if self.cleaned_data.get('spots_left'):
        #     qs = qs.exclude(spots=F('filled'))

        if self.cleaned_data.get('keywords'):
            keywords = [a.lower() for a in keyword_regex.findall(self.cleaned_data['keywords'])]
            for kw in keywords:
                qs = qs.filter(Q(description__icontains=kw) | Q(course__name__icontains=kw))
            qs = qs.distinct()

        qs = qs.order_by('code_slug'), term
        return qs

class ScheduleForm(forms.Form):
    key = forms.CharField(max_length=100)


class ICalExportForm(forms.Form):
    start = forms.DateField(label="First day of classes")
    end = forms.DateField(label="Last day of classes")

    def clean_end(self):
        if not (self.cleaned_data.get('start') and self.cleaned_data.get('end')):
            raise forms.ValidationError("You must specify both start and end dates")
        start, end = self.cleaned_data['start'], self.cleaned_data['end']
        if end > start:
            return end
        else:
            raise forms.ValidationError("The last day of the semester "
                                        "must be after the first day of classes.")

class ReviewSearchForm(forms.Form):
	object_type = forms.ChoiceField(
		required=False,
		choices=[('course', 'courses'), ('professor', 'professors')],
		widget=forms.Select(attrs={'id': 'object_type_dropdown'})
	)
	department = DeptModelChoice(
		required=False,
		queryset=Department.objects.annotate(num_courses=Count('course_set')).filter(num_courses__gt=0).distinct().order_by('code'),
		empty_label="(any)"
	)
	course_name_or_number = forms.CharField(
		required=False,
		max_length=100,
		widget=forms.TextInput(attrs={'size': '40', 'placeholder': 'e.g. "Intro Biology" or "001A"'})
	)
	professor_name = forms.CharField(
		required=False,
		max_length=100,
		widget=forms.TextInput(attrs={'size': '40', 'placeholder': 'e.g. "David Oxtoby"'})
	)

	def build_queryset(self):
		if self.cleaned_data['object_type'] == 'course':
			qs = Course.objects.all()

			if self.cleaned_data.get('department'):
				qs = qs.filter(departments=self.cleaned_data['department'])

			if self.cleaned_data.get('course_name_or_number'):
				keyword_tokens = self.cleaned_data['course_name_or_number'].split()
				for k in keyword_tokens:
					qs = qs.filter(Q(name__icontains=k) | Q(code__icontains=k))

			return qs.distinct(), 'course'
		elif self.cleaned_data['object_type'] == 'professor':
			department_instructors = []
			filtered_instructors = []

			if self.cleaned_data.get('department'):
				section_objects = Section.objects.filter(course__departments=self.cleaned_data['department'])
				for s in section_objects:
					for i in s.instructors.all():
						department_instructors.append(i)
				department_instructors = list(set(department_instructors))

			if self.cleaned_data.get('professor_name'):
				name_tokens = re.split('(?!-)\W+', self.cleaned_data['professor_name'])
				filtered_instructors = list(Instructor.objects.filter(
					reduce(
						operator.and_,
						(Q(name__icontains=nt) for nt in name_tokens)
					)
				).distinct())

			to_return = None

			if department_instructors and filtered_instructors:
				# Return the intersection of both lists
				to_return = list(set(department_instructors) & set(filtered_instructors))
			elif department_instructors:
				to_return = department_instructors
			elif filtered_instructors:
				to_return = filtered_instructors
			else:
				to_return = list(Instructor.objects.all().distinct())

			to_return.sort(key=operator.attrgetter('name'))
			return to_return, 'instructor'
		else:
			return [], ''

class ReviewForm(forms.Form):
    CHOICES = [(i,i) for i in range(1,6)]
    overall_rating = forms.ChoiceField(choices=CHOICES, label='How many stars do you give this class?')
    useful_rating = forms.ChoiceField(choices=CHOICES, label='How useful was this class?', help_text='1: This course was irrelevant for me <br />5: I use what I learned in this course every day')
    engagement_rating = forms.ChoiceField(choices=CHOICES, label='How engaging was this class?', help_text='1: I fell asleep every day <br />5: I couldn\'t stop thinking about this course')
    difficulty_rating = forms.ChoiceField(choices=CHOICES, label='How difficult was this class?', help_text='1: I could do the homework in my sleep <br />5: I still don\'t understand what I did in this course')
    competency_rating = forms.ChoiceField(choices=CHOICES, label='How competent was the professor?', help_text='1: The prof had no clue <br />5: The prof knew the material backwards and forwards')
    lecturing_rating = forms.ChoiceField(choices=CHOICES, label='How was the professor\'s lecturing style?', help_text='1: Lectures were poorly planned and delivered <br />5: I remember every word the prof said')
    enthusiasm_rating = forms.ChoiceField(choices=CHOICES, label='How enthusiastic was the professor?', help_text='1: I would rather speak to Darth Vader <br />5: I consider this prof a personal friend')
    approachable_rating = forms.ChoiceField(choices=CHOICES, label='How approachable was the professor?', help_text='1: The prof had no pulse <br />5: The prof\'s excitement was infectious')
    work_per_week = forms.IntegerField(max_value=25, label='How many hours of work did you have each week?')
    comments = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '15'}), label='General comments:')

    def __init__(self, course_code, review=None, *args, **kwargs):
      super(ReviewForm, self).__init__(*args, **kwargs)
      self.course = Course.objects.get(code_slug=course_code)
      instructors = self.course.get_instructors_from_all_sections()
      self.fields['professor'] = forms.ModelChoiceField(queryset=Instructor.objects.filter(pk__in=map(lambda u: u.id, instructors)))
      def smart_int(rating):
          if rating:
              return int(rating)
          else:
              return 1
      if review:
        self.initial['professor'] = review.instructor
        self.initial['overall_rating'] = int(review.overall_rating)
        self.initial['work_per_week'] = review.work_per_week
        self.initial['useful_rating'] = smart_int(review.useful_rating)
        self.initial['engagement_rating'] = smart_int(review.engagement_rating)
        self.initial['difficulty_rating'] = smart_int(review.difficulty_rating)
        self.initial['competency_rating'] = smart_int(review.competency_rating)
        self.initial['lecturing_rating'] = smart_int(review.lecturing_rating)
        self.initial['approachable_rating'] = smart_int(review.approachable_rating)
        self.initial['enthusiasm_rating'] = smart_int(review.enthusiasm_rating)
        self.initial['comments'] = review.comments
    def course(self):
      return self.course