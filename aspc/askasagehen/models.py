from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	author = models.ForeignKey(User)
	title = models.TextField()
	body = models.TextField()
	post_timestamp = models.DateTimeField(editable=False, auto_now_add=True)
	last_edit_timestamp = models.DateTimeField(editable=False, auto_now=True)
	votes = models.IntegerField()

class Answer(models.Model):
	question = models.ForeignKey(Question)
	author = models.ForeignKey(User)
	body = models.TextField()
	post_timestamp = models.DateTimeField(editable=False, auto_now_add=True)
	last_edit_timestamp = models.DateTimeField(editable=False, auto_now=True)
	votes = models.IntegerField()