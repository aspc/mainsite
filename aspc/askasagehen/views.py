from django.shortcuts import render

# /askasagehen
def home (request):
	if request.method == 'GET':
		return render(request, 'askasagehen/home.html', {})