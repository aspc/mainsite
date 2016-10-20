import logging
from django.db import models
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

COLLEGES = (
	('POM', 'Pomona'),
	('CMC', 'Claremont McKenna'),
	('SC', 'Scripps'),
	('PZ', 'Pitzer'),
	('HMC', 'Harvey Mudd')
)

DEFAULT_COLLEGE = 'POM'

EMAIL_SUFFIXES = {
	'POM': 'pomona.edu',
	'CMC': 'cmc.edu',
	'SC': 'scrippscollege.edu',
	'PZ': 'students.pitzer.edu',
	'HMC': 'hmc.edu'
}

# UserData holds auxiliary data associated with users that is not directly releated to authentication, per the
# Django 1.7 spec here: https://docs.djangoproject.com/en/1.7/topics/auth/customizing/#specifying-a-custom-user-model
#
# Since the switch to the auth2 backend, the `college` field is necessary for differentiating 5C users
# Access to `year` and `dorm` attributes are still in the pipeline from ITS
class UserData(models.Model):
	user = models.ForeignKey(User, null=False, blank=False, related_name='user')
	full_name = models.CharField(max_length=255, null=True, blank=True)
	college = models.CharField(max_length=255, null=False, blank=False, choices=COLLEGES, default=DEFAULT_COLLEGE)
	is_faculty = models.BooleanField(default=False)
	year = models.IntegerField(null=True, blank=True)
	dorm = models.CharField(max_length=255, null=True, blank=True)
	subscribed_email = models.BooleanField(default=True)

	# Returns what college a user belongs to, based on his email suffix
	@staticmethod
	def belongs_to_college(user):
		if user.email:
			try:
				return (college for college, suffix in EMAIL_SUFFIXES.items() if suffix in user.email).next()
			except StopIteration:
				logger.error('Invalid email address for user: %s' % user.email)
				return DEFAULT_COLLEGE
		else:
			return DEFAULT_COLLEGE

	class Meta:
		verbose_name_plural = 'user data'
