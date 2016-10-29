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
    CHOICES = [(i,i) for i in range(1,6)]
    therapist = forms.ChoiceField(choices=CHOICES, label='How many stars do you give this class?')
    reasons = forms.ChoiceField(choices=CHOICES, label='How useful was this class?', help_text='1: This course was irrelevant for me <br />5: I use what I learned in this course every day')
    duration = forms.ChoiceField(choices=CHOICES, label='How engaging was this class?', help_text='1: I fell asleep every day <br />5: I couldn\'t stop thinking about this course')
    feeling = forms.ChoiceField(choices=CHOICES, label='How difficult was this class?', help_text='1: I could do the homework in my sleep <br />5: I still don\'t understand what I did in this course')
    gender = forms.ChoiceField(choices=CHOICES, label='How competent was the professor?', help_text='1: The prof had no clue <br />5: The prof knew the material backwards and forwards')
    sexual_orientation = forms.ChoiceField(choices=CHOICES, label='How was the professor\'s lecturing style?', help_text='1: Lectures were poorly planned and delivered <br />5: I remember every word the prof said')
    ethnicity = forms.ChoiceField(choices=CHOICES, label='How enthusiastic was the professor?', help_text='1: The prof had no pulse <br />5: The prof\'s excitement was infectious')
    identity = forms.ChoiceField(choices=CHOICES, label='How approachable was the professor?', help_text='1: I would rather speak to Darth Vader <br />5: I consider this prof a personal friend')
    identity_related_comment = forms.IntegerField(max_value=25, label='How many hours of work did you have each week?')
    therapist_recommendation = forms.ChoiceField(choices=POSSIBLE_GRADES_OPTIONS, required=False)
    therapist_strategy = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '15'}), label='General comments:')
    tags = ...



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