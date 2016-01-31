from django.contrib import admin
from aspc.files.models import ImageUpload, FileUpload

class ImageUploadAdmin(admin.ModelAdmin):
	list_display = ('name', 'image')

class FileUploadAdmin(admin.ModelAdmin):
	list_display = ('name', '_file')

admin.site.register(ImageUpload, ImageUploadAdmin)
admin.site.register(FileUpload, FileUploadAdmin)