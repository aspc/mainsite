from django.shortcuts import render
from django.http import HttpResponseRedirect
from aspc.askasagehen.models import Question
from aspc.askasagehen.forms.forms import QuestionForm

# /askasagehen
def home (request):
	if request.method == 'GET':
		return render(request, 'askasagehen/home.html', {'questions': Question.objects.all()})

def question (request, question_id):
	if request.method == 'GET' and question_id: # Render an existing question
		return render(request, 'askasagehen/question.html', {'question': Question.objects.get(id=question_id)})
	elif request.method == 'GET': # Render the question submssion form
		form = QuestionForm()
		return render(request, 'askasagehen/submit_question.html', {'form': form})
	elif request.method == 'POST': # Process the submitted form
		form = QuestionForm(request.POST)
		if form.is_valid():
			form.instance.author = request.user
			form.save()
			return HttpResponseRedirect('/askasagehen/')