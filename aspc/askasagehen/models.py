from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length=255)
	body = models.TextField()
	post_timestamp = models.DateTimeField(editable=False, auto_now_add=True)
	last_edit_timestamp = models.DateTimeField(editable=False, auto_now=True)
	votes = models.IntegerField(default=0)
	category_is_academic = models.BooleanField(default=False)
	category_is_housing = models.BooleanField(default=False)
	category_is_administrative = models.BooleanField(default=False)
	category_is_social = models.BooleanField(default=False)

class Answer(models.Model):
	question = models.ForeignKey(Question)
	author = models.ForeignKey(User)
	body = models.TextField()
	post_timestamp = models.DateTimeField(editable=False, auto_now_add=True)
	last_edit_timestamp = models.DateTimeField(editable=False, auto_now=True)
	votes = models.IntegerField(default=0)