from django.forms import Form, ModelForm, CheckboxSelectMultiple, ModelMultipleChoiceField, ChoiceField, RadioSelect

from aspc.forum.models import Post, Question, Answer, Tag


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author','created_ts']
        widgets = {
            'tags': CheckboxSelectMultiple
        }
        labels = {
        	'tags': 'Choose tags for your post',
            'anonymous': 'I don\'t want to be contacted, even if it\'s anonymous'
        }


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ['author','created_ts']
        widgets = {
            'tags': CheckboxSelectMultiple
        }
        labels = {
            'tags': 'Choose tags for your post'
        }

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ['author','created_ts','question']

class SearchForm(Form):
    tags = ModelMultipleChoiceField(queryset=Tag.objects, widget=CheckboxSelectMultiple)
    choices = (('Post', 'Search posts'),('Question', 'Search questions'))
    search_page = ChoiceField(choices=choices, widget=RadioSelect)
