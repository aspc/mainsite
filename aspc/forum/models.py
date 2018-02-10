from __future__ import unicode_literals

import django
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=300, unique=True)
	def __unicode__(self):
		return self.name

class Post(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length=200)
	created_ts = models.DateTimeField(default=django.utils.timezone.now)
	text = models.TextField()
	tags = models.ManyToManyField(Tag, blank=True)
class Question(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length=200)
	created_ts = models.DateTimeField(default=django.utils.timezone.now)
	text = models.TextField()
	tags = models.ManyToManyField(Tag, blank=True)
class Answer(models.Model):
	author = models.ForeignKey(User)
	created_ts = models.DateTimeField(default=django.utils.timezone.now)
	question = models.ForeignKey(Question, related_name='answers')
	text = models.TextField()
