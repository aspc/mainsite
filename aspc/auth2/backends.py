import logging
from urllib import urlencode, urlopen
from urlparse import urljoin
from xml.dom import minidom
from xml.etree import ElementTree
from django.conf import settings
from django.contrib.auth.models import User
from aspc.auth2.models import UserData
from aspc.auth2.exceptions import CASTicketException

__all__ = ['CASBackend']

logger = logging.getLogger(__name__)

# CAS authentication backend, authenticating against the 5C CAS server
class CASBackend(object):
	supports_object_permissions = False
	supports_inactive_user = False

	# Vertifies CAS ticket and gets or creates User, UserData objects
	# A user's attributes are refreshed every time he logs in (particularly important for the `year` and `dorm` attributes)
	def authenticate(self, ticket, service):
		try:
			user_info = _verify_cas(ticket, service)
		except Exception as e:
			logger.error('Failed to verify CAS authentication', e)
			return None

		# Store user data associated with authenticate in the generic User model
		user, is_new = User.objects.get_or_create(username__iexact=user_info['username'])
		user.username = user_info['username']
		user.first_name = user_info['first_name']
		user.last_name = user_info['last_name']
		user.email = user_info['email']
		user.save()

		# Store auxiliary user data like the college in the UserData model
		user_data, is_new = UserData.objects.get_or_create(user=user)
		user_data.college = UserData.belongs_to_college(user)
		user_data.year = None
		user_data.dorm = None
		user_data.save()

		return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

# Verifies CAS 2.0+ XML-based authentication ticket
# Returns complete user data dictionary on success and raises an exception on failure
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
	user_info = {
		'username': '',
		'first_name': '',
		'last_name': '',
		'email': ''
	}

	try:
		page = urlopen(url)
		response = page.read()
		tree = ElementTree.fromstring(response)
		document = minidom.parseString(response)
	except Exception as e:
		raise CASTicketException('Failed to open CAS ticket: ' + e)

	if document.getElementsByTagName('cas:authenticationSuccess'):
		user_info['last_name'] = (document.getElementsByTagName('cas:lastName') or [None])[0].text
		user_info['email'] = (document.getElementsByTagName('cas:email') or [None])[0].text
		user_info['username'] = (document.getElementsByTagName('cas:fullName') or [None])[0].text
		user_info['first_name'] = (document.getElementsByTagName('cas:firstName') or [None])[0].text

		if not all(user_info.values()):
			raise CASTicketException('CAS ticket missing attributes: %s' % str(user_info))
	elif document.getElementsByTagName('cas:authenticationFailure'):
		error_message = document.getElementsByTagName('cas:authenticationFailure')[0].firstChild.nodeValue
		raise CASTicketException('Authentication failed from CAS server: %s' % error_message)
	else:
		raise CASTicketException('No standard authentication status response: %s' % str(response))

	return user_info