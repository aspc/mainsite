from django.db import models

class ImageUpload(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField()

class FileUpload(models.Model):
	name = models.CharField(max_length=100)
	_file = models.FileField()  # `file` is a built-in Python function