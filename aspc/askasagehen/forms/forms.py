from django.forms import ModelForm
from aspc.askasagehen.models import Question, Answer

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body', 'category_is_academic', 'category_is_housing', 'category_is_administrative', 'category_is_social']

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['body']