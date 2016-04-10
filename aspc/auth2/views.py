from urllib import urlencode, quote_plus, unquote
import urlparse
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from aspc import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

__all__ = ['guest_login', 'login', 'logout']
PHP_AUTH_URL = 'https://aspc.pomona.edu/php-auth'

## GUEST LOGIN - Uses django.contrib.auth.backends.ModelBackend for authentication
# Endpoint has two functions:
# 1) On GET, renders a login form for guest accounts (i.e. users that are backed locally, not in the 5C CAS server)
# 2) On POST, validates the login form, authenticates the user, and logs him in
def guest_login(request, next_page=None):
	next_page = next_page or _next_page_url(request)

	if request.method == 'GET':
		# If the user is already authenticated, simply redirect to the next_page
		if request.user.is_authenticated():
			return HttpResponseRedirect(unquote(next_page))
		else:
			form = AuthenticationForm()
			return render(request, 'auth2/guest_login.html', {'form': form, 'next': next_page})
	elif request.method == 'POST':
		from django.contrib import auth
		form = AuthenticationForm(data=request.POST)

		if form.is_valid():
			user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

			if user is not None:
				auth.login(request, user)
				return HttpResponseRedirect(unquote(next_page))
			else:
				return render(request, 'auth2/guest_login.html', {'form': form})
		else:
			return render(request, 'auth2/guest_login.html', {'form': form})
	else:
		return HttpResponseNotAllowed(['GET', 'POST'])

## CAS LOGIN - Uses aspc.auth2.backends.CASBackend for authentication
# Endpoint has two functions:
# 1) Forwards to CAS login URL upon first login
# 2) Validates a CAS ticket upon receipt from the CAS server
def login(request, next_page=None):
	if request.method == 'GET':
		next_page = next_page or _next_page_url(request)

		# If the user is already authenticated, simply redirect to the next_page
		if request.user.is_authenticated():
			# Redirect via the PHP login script though to ensure that the session hasn't expired there
			return HttpResponseRedirect(PHP_AUTH_URL + '/login.php?redirect=' + quote_plus(next_page))

		ticket = request.GET.get('ticket')

		# Required to authenticate over SSL
		# Also pass along the next_page reference so we can pick it up again on the ticket response
		service_url = 'https://' + request.get_host() + request.path + '?next=' + quote_plus(next_page)

		# If there is already a ticket, perform validation on it
		if ticket:
			from django.contrib import auth
			user = auth.authenticate(ticket=ticket, service=service_url)

			if user is not None:
				# Ticket successfully validated and user data retrieved - perform login
				auth.login(request, user)

				# Redirect to a PHP script to complete PHP session login on that side
				# Afterwards, the PHP script will redirect to the ASPC index page or next_page if set
				return HttpResponseRedirect(PHP_AUTH_URL + '/login.php?redirect=' + quote_plus(next_page))
			else:
				# Some error in the ticket validation - try the login again
				return HttpResponseRedirect(_login_url(service_url))
		# Otherwise it is the first login - redirect to the CAS login URL
		else:
			return HttpResponseRedirect(_login_url(service_url))
	else:
		return HttpResponseNotAllowed(['GET'])

# Performs user logout
def logout(request, next_page=None):
	if request.method == 'GET':
		# Do nothing if someone who is already logged out tries to log out again
		if request.user.is_anonymous():
			return HttpResponseRedirect('/')

		from django.contrib.auth import logout
		next_page = next_page or _next_page_url(request)
		is_guest = request.user.has_usable_password()

		# If the user is not a guest user (i.e. is logged in via CAS), we will have to redirect to the
		# CAS service to complete federated logout there
		if not is_guest:
			next_page = _logout_url()

		# But first, log the local Django user out
		logout(request)

		# And then redirect to a PHP script to complete PHP session logout on that side
		# Afterwards, the PHP script will redirect to next_page (either the CAS logout or the homepage, depending
		# on the boolean fork above with is_guest)
		return HttpResponseRedirect(PHP_AUTH_URL + '/logout.php?redirect=' + quote_plus(next_page))
	else:
		return HttpResponseNotAllowed(['GET'])

# Redirects to referring page, or to the homepage if no referrer is set
def _next_page_url(request):
	next_page = '/'

	if request.method == 'GET':
		return request.GET.get(REDIRECT_FIELD_NAME) or next_page
	elif request.method == 'POST':
		return request.POST.get(REDIRECT_FIELD_NAME) or next_page
	else:
		return next_page

# Builds CAS login URL
def _login_url(service_url):
	params = {
		'service': service_url
	}

	return urlparse.urljoin(settings.CAS_SETTINGS['SERVER_URL'], 'login') + '?' + urlencode(params)

# Builds CAS logout URL
def _logout_url():
	return urlparse.urljoin(settings.CAS_SETTINGS['SERVER_URL'], 'logout')