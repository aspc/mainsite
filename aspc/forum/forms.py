from django.forms import ModelForm#, CheckboxSelectMultiple

from aspc.forum.models import Post, Question, Answer


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author','created_ts']


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ['author','created_ts']

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ['author','created_ts','question']