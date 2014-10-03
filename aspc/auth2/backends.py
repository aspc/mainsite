import logging
from urllib import urlencode, urlopen
from urlparse import urljoin
from xml.dom import minidom
from xml.etree import ElementTree
from django.conf import settings
from django.contrib.auth.models import User

__all__ = ['CASBackend']

logger = logging.getLogger(__name__)

# CAS authentication backend, authenticating against the 5C CAS server
class CASBackend(object):
	supports_object_permissions = False
	supports_inactive_user = False

	# Vertifies CAS ticket and gets or creates User object
	def authenticate(self, ticket, service):
		return _verify_cas(ticket, service)
		username = _verify_cas(ticket, service)
		if not username:
			return None
		try:
			user = User.objects.get(username__iexact=username)
		except User.DoesNotExist:
			user = User(
				username=username,
				first_name=None,
				last_name=None,
				email=None,
			)
			user.set_unusable_password()
			user.save()
		return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

# Verifies CAS 2.0+ XML-based authentication ticket
# Returns username on success and None on failure
def _verify_cas(ticket, service):
	params = {
		'ticket': ticket,
		'service': service
	}

	url = urljoin(settings.CAS_SETTINGS['SERVER_URL'], 'serviceValidate') + '?' + urlencode(params)
	page = urlopen(url)
	username = None

	try:
		response = page.read()
		tree = ElementTree.fromstring(response)
		document = minidom.parseString(response)

		#Useful for debugging
		#print document.toprettyxml()

		if tree[0].tag.endswith('authenticationSuccess'):
			username = tree[0][0].text

		else:
			failure = document.getElementsByTagName('cas:authenticationFailure')
			if failure:
				logger.warn('Authentication failed from CAS server: %s', failure[0].firstChild.nodeValue)

	except Exception as e:
		logger.error('Failed to verify CAS authentication', e)

	finally:
		page.close()

	return str(response)