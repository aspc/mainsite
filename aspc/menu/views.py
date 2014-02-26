from django.shortcuts import render

# /menu
def home (request):
	if request.method == 'GET': # Render the menu index on GET
		return render(request, 'menu/home.html', {})