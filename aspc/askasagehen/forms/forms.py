from django.forms import ModelForm
from aspc.askasagehen.models import Question

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']