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
		user_data = _verify_cas(ticket, service)
		if not user_data['username']:
			return None
		try:
			user = User.objects.get(username__iexact=user_data['username'])
		except User.DoesNotExist:
			user = User(
				username=user_data['username'],
				first_name=user_data['first_name'],
				last_name=user_data['last_name'],
				email=user_data['email']
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
# Returns user data on success and None on failure
#
# Example response:
#
# <cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>
#	<cas:authenticationSuccess>
#	<!-- Begin Ldap Attributes -->
#		<cas:attributes>
#			<cas:lastName>Dahl</cas:lastName>
#			<cas:EmailAddress>mdd32013@MyMail.pomona.edu</cas:EmailAddress>
#			<cas:fullName>mdd32013</cas:fullName>
#			<cas:firstName>Matthew</cas:firstName>
#		</cas:attributes>
#	<!-- End Ldap Attributes -->
#	</cas:authenticationSuccess>
# </cas:serviceResponse>
def _verify_cas(ticket, service):
	params = {
		'ticket': ticket,
		'service': service
	}

	url = urljoin(settings.CAS_SETTINGS['SERVER_URL'], 'serviceValidate') + '?' + urlencode(params)
	page = urlopen(url)
	user_data = {
		'username': '',
		'first_name': '',
		'last_name': '',
		'email': ''
	}

	try:
		response = page.read()
		tree = ElementTree.fromstring(response)
		document = minidom.parseString(response)

		if tree[0].tag.endswith('authenticationSuccess'):
			user_data['last_name'] = tree[0][0][0].text
			user_data['email'] = tree[0][0][1].text
			user_data['username'] = tree[0][0][2].text
			user_data['first_name'] = tree[0][0][3].text

		else:
			failure = document.getElementsByTagName('cas:authenticationFailure')
			if failure:
				logger.warn('Authentication failed from CAS server: %s', failure[0].firstChild.nodeValue)

	except Exception as e:
		logger.error('Failed to verify CAS authentication', e)

	finally:
		page.close()

	return user_data