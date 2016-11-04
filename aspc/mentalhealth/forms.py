from django import forms
# Need implementation
#from aspc.courses.models import (Department, Section, Meeting, Term, Course, Instructor,
#                                 RequirementArea, CAMPUSES, CAMPUSES_FULL_NAMES, CAMPUSES_LOOKUP, POSSIBLE_GRADES)
from django.db.models import Count, F

import re
from itertools import groupby
from django.forms.widgets import Widget, Select
from django.forms.models import ModelChoiceIterator
from django.utils.safestring import mark_safe
from django.db.models import Q
import operator

class ReviewForm(forms.Form):
	# Need modification
    # Use charField
    # Need to be changed
    CHOICES = [(i,i) for i in range(1,6)]
    therapist = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '1'}), label='Name of the therapist:')
    reasons = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '3'}), label='Reason for therapy:')
    # Need to be changed
    duration = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '1'}), label='Duration:')
    # choices
    feeling = forms.ChoiceField(choices=CHOICES, label='What is your feeling')
    # choices
    gender = forms.ChoiceField(choices=CHOICES, label='What is your gender')
    # choices
    sexual_orientation = forms.ChoiceField(choices=CHOICES, label='What is your sexual_orientation')
    ethnicity = forms.ChoiceField(choices=CHOICES, label='What is your ethnicity')
    identity = forms.ChoiceField(choices=CHOICES, label='What is your identity')
    identity_related_comment = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '3'}), label='Comment related to identity')
    therapist_recommendation = forms.ChoiceField(choices=CHOICES)
    therapist_strategy = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '3'}), label='Therapist_strategy:')
    #tags = ...



    def __init__(self, therapist_id, review=None, *args, **kwargs):
      super(ReviewForm, self).__init__(*args, **kwargs)
      self.therapist = Therapist.objects.get(code_slug=course_code) # How does this work
      #self.fields['professor'] = forms.ModelChoiceField(queryset=Instructor.objects.filter(pk__in=map(lambda u: u.id, instructors)))
      if review:
        self.initial['therapist'] = review.therapist
        self.initial['reasons'] = review.reasons
        self.initial['duration'] = review.duration
        self.initial['feeling'] = review.feeling
        self.initial['gender'] = sreview.gender
        self.initial['sexual_orientation'] = review.sexual_orientation
        self.initial['ethnicity'] = review.ethnicity
        self.initial['identity'] = review.identity
        self.initial['identity_related_comment'] = review.identity_related_comment
        self.initial['therapist_recommendation'] = review.therapist_recommendation
        self.initial['therapist_strategy'] = review.therapist_strategy
        self.initial['tags'] = review.tags
    def therapist(self):
      return self.therapist