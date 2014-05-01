from django.shortcuts import render
from aspc.askasagehen.models import Question

# /askasagehen
def home (request):
	if request.method == 'GET':
		return render(request, 'askasagehen/home.html', {'questions': Question.objects.all()})