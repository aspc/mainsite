from django.shortcuts import render
from django.http import HttpResponseRedirect
from aspc.askasagehen.models import Question, Answer
from aspc.askasagehen.forms.forms import QuestionForm, AnswerForm

# /askasagehen
def home (request):
	if request.method == 'GET':
		return render(request, 'askasagehen/home.html', {
			'latest_question': Question.objects.latest('post_timestamp'),
			'latest_academic_questions': Question.objects.filter(category_is_academic=True).order_by('post_timestamp')[:5],
			'latest_housing_questions': Question.objects.filter(category_is_housing=True).order_by('post_timestamp')[:5],
			'latest_administrative_questions': Question.objects.filter(category_is_administrative=True).order_by('post_timestamp')[:5],
			'latest_social_questions': Question.objects.filter(category_is_social=True).order_by('post_timestamp')[:5]
		})

def question (request, question_id):
	if request.method == 'GET' and question_id: # Render an existing question
		return render(request, 'askasagehen/question.html', {
			'question': Question.objects.get(id=question_id),
			'answers': Answer.objects.filter(question_id=question_id),
			'answer_form': AnswerForm()
		})
	elif request.method == 'GET': # Render the question submssion form
		return render(request, 'askasagehen/submit_question.html', {'question_form': QuestionForm()})
	elif request.method == 'POST': # Process the submitted form
		form = QuestionForm(request.POST)
		if form.is_valid():
			form.instance.author = request.user
			form.save()
			return HttpResponseRedirect('/askasagehen/')

def answer (request, question_id):
	if request.method == 'POST': # Process the submitted form
		form = AnswerForm(request.POST)
		if form.is_valid():
			form.instance.author = request.user
			form.instance.question = Question.objects.get(id=question_id)
			form.save()
			return HttpResponseRedirect('/askasagehen/question/' + question_id)