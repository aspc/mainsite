from django.contrib import admin
from aspc.forum.models import (Tag, Answer, Question, Post)

admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Post)