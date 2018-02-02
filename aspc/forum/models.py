from __future__ import unicode_literals

from django.db import models

# Create your models here.
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
    question = modes.ForeignKey(Question, related_name='answers')
    text = models.TextField()
    question_id = models.IntegerField()
   