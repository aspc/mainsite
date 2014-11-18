from django import forms
from aspc.courses.models import (Department, Section, Meeting, Term,
                                 RequirementArea, CAMPUSES, CAMPUSES_FULL_NAMES, CAMPUSES_LOOKUP)
from django.db.models import Count, F

import re
from itertools import groupby
from django.forms.widgets import Widget, Select
from django.forms.models import ModelChoiceIterator
from django.utils.safestring import mark_safe


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
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    (self.field.group_label(group), [self.choice(ch) for ch in choices])
                    for group, choices in groupby(self.queryset.all(),
                                                  key=lambda row: getattr(row, self.field.group_by_field))
                ]
            for choice in self.field.choice_cache:
                yield choice
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

    def build_queryset(self):
        qs = Section.objects.filter(term=self.cleaned_data['term'])
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
            qs = qs.filter(instructors__name__icontains=self.cleaned_data['instructor'])
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
            qs_descfilter = qs
            qs_namefilter = qs
            for kw in keywords:
                qs_descfilter = qs_descfilter.filter(description__icontains=kw)
                qs_namefilter = qs_namefilter.filter(course__name__icontains=kw)
            qs = (qs_descfilter or qs_namefilter)
            qs = qs.distinct()

        qs = qs.distinct('code_slug').order_by('code_slug')
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
