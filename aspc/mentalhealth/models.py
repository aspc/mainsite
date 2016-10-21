from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name

class Insurance(Category):
    pass

class Qualification(Category):
    pass

class Specialty(Category):
    pass

class Tag(Category):
    pass

class Gender(Category):
    pass

class Identity(Category):
    pass

class SexualOrientation(Category):
    pass

class Ethnicity(Category):
    pass

class Therapist(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    address = models.CharField(max_length=100, unique=True, null=True, blank=True)
    website = models.CharField(max_length=100, unique=True, null=True, blank=True)
    insurances = models.ManyToManyField(Insurance)
    specialties = models.ManyToManyField(Specialty)
    qualifications = models.ManyToManyField(Qualification)

    def __unicode__(self):
        return self.name

class MentalHealthReview(models.Model):
    reviewer = models.ForeignKey(User)
    therapist = models.ForeignKey(Therapist)
    reasons = models.ManyToManyField(Specialty)
    duration = models.TextField()
    feeling = models.TextField()
    gender = models.ManyToManyField(Gender)
    sexual_orientation = models.ManyToManyField(SexualOrientation)
    ethnicity = models.ManyToManyField(Ethnicity)
    identity = models.ManyToManyField(Identity)
    identity_related_comment = models.TextField(null=True, blank=True)
    therapist_recommendation = models.TextField()
    therapist_strategy = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_ts = models.DateTimeField(default=datetime.now)

