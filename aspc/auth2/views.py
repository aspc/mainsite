from urllib import urlencode
import urlparse
from django.http import HttpResponseRedirect
from aspc import settings
from django.contrib.auth import REDIRECT_FIELD_NAME

__all__ = ['login', 'logout']

# Endpoint has two functions:
# 1) Forwards to CAS login URL upon first login
# 2) Validate a CAS ticket upon receipt from the CAS server
def login(request, next_page=None):
	next_page = next_page or _next_page_url(request)

	# If the user is already authenticated, simply redirect to the next_page
	if request.user.is_authenticated():
		return HttpResponseRedirect(next_page)

	ticket = request.GET.get('ticket')
	service_url = 'https://' + request.get_host() + request.path  # Required to authenticate over SSL

	# If there is already a ticket, perform validation on it
	if ticket:
		from django.contrib import auth
		xml = auth.authenticate(ticket=ticket, service=service_url)
		return HttpResponseRedirect('https://staging.aspc.pomona.edu?' + xml)

		if user is not None:
			# Ticket successfully validated and user data retrieved - perform login
			auth.login(request, user)
			return HttpResponseRedirect('https://staging.aspc.pomona.edu?' + user.username)
		else:
			# Some error in the ticket validation - try the login again
			return HttpResponseRedirect(_login_url(service_url))
	# Otherwise it is the first login - redirect to the CAS login URL
	else:
		return HttpResponseRedirect(_login_url(service_url))

# Performs user logout
def logout(request, next_page=None):
	from django.contrib.auth import logout
	next_page = next_page or _next_page_url(request)

	# First logout the local Django user
	logout(request)

	# Then perform a redirection to the CAS server to complete logout there
	return HttpResponseRedirect(_logout_url())

# Redirects to referring page, or to the homepage if no referrer is set.
def _next_page_url(request):
	next_page = request.GET.get(REDIRECT_FIELD_NAME) or ''
	host = request.get_host()
	prefix = (('http://', 'https://')[request.is_secure()] + host)
	if next_page.startswith(prefix):
		next_page = next[len(prefix):]
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