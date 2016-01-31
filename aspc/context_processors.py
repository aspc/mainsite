from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from django.conf import settings as aspc_settings
import re

# Auxiliary request data to pass to templates
def request(request):
	port_string = request.META.get('SERVER_PORT')
	user_agent = request.META.get('HTTP_USER_AGENT') or request.META.get('HTTP_AGENT')

	site_info = {
		'protocol': request.is_secure() and 'https' or 'http',
		'port': port_string if port_string != "80" else None,
		'absolute_uri': request.build_absolute_uri(),
		'domain': Site.objects.get_current().domain if Site._meta.installed else RequestSite(request).domain,
		'is_mobile': bool(re.search(
			'Android|BlackBerry|iPhone|iPad|iPod|Opera Mini|IEMobile|SymbianOS|Windows Phone|Mobile',
			user_agent,
			re.IGNORECASE
		)) if user_agent else False
	}

	return site_info

# settings.py data to pass to templates
def settings(request):
	return {
		'voting_active': aspc_settings.VOTING_ACTIVE
	}