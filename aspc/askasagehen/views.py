from django.shortcuts import render
from django.http import HttpResponseRedirect
from aspc.askasagehen.models import Question
from aspc.askasagehen.forms.forms import QuestionForm

# /askasagehen
def home (request):
	if request.method == 'GET':
		return render(request, 'askasagehen/home.html', {'questions': Question.objects.all()})

def question (request):
	if request.method == 'POST': # If the form has been submitted...
		form = QuestionForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			form.instance.author = request.user
			form.save()
			return HttpResponseRedirect('/askasagehen/')
	elif request.method == 'GET':
		form = QuestionForm()
		return render(request, 'askasagehen/submit_question.html', {'form': form})