import os, django

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

ADMINS = (
	('Digital Media Group', 'digitalmedia@aspc.pomona.edu'),
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# A list of strings representing the host/domain names that this Django site
# can serve. This is a security measure to prevent an attacker from poisoning
# caches and password reset emails with links to malicious hosts by
# submitting requests with a fake HTTP Host header, which is possible even
# under many seemingly-safe web server configurations.
ALLOWED_HOSTS = (
	'aspc.pomona.edu',
	'aspc.pomona.edu.',
	'.aspc.pomona.edu',
	'.aspc.pomona.edu.', # allow FQDN (with trailing dot)
)

# Use this in case of disallowed host exception
#ALLOWED_HOSTS = ['*']

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Additional locations of static files
STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_ROOT, 'static'),
)

# Boolean that decides if compression should also be done outside of the request/response loop -
# independent from user requests. This allows to pre-compress CSS and JavaScript files and works
# just like the automatic compression with the {% compress %} tag.
# http://django-compressor.readthedocs.org/en/latest/settings/?highlight=cache#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True

# Controls the directory inside COMPRESS_ROOT that compressed files will be written to.
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OUTPUT_DIR
COMPRESS_OUTPUT_DIR = 'compressed'

# Compression filters to apply to the concatenated JS (e.g. minifications)
# http://django-compressor.readthedocs.org/en/latest/settings/?highlight=cache#django.conf.settings.COMPRESS_JS_FILTERS
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]

# Compression filters to apply to the concatenated CSS (e.g. minifications)
# http://django-compressor.readthedocs.org/en/latest/settings/?highlight=cache#django.conf.settings.COMPRESS_CSS_FILTERS
COMPRESS_CSS_FILTERS = [
    'compressor.filters.cssmin.rCSSMinFilter'
]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "aspc.context_processors.request",
    "aspc.context_processors.settings"
)

MIDDLEWARE_CLASSES = (
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'corsheaders.middleware.CorsPostCsrfMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'aspc.auth2.middleware.CASMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'aspc.urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'django.contrib.redirects',
	'django.contrib.humanize',
	"geoposition",
	'gunicorn',
	'django_extensions',
	'debug_toolbar',
    'rest_framework',
    'rest_framework.authtoken',
	'corsheaders',
	'stdimage',
	'adminsortable2',
	'compressor',
	'aspc.folio',
	'aspc.senate',
	'aspc.blog',
    'aspc.api',
	'aspc.auth1',
	'aspc.auth2',
	'aspc.sagelist',
	'aspc.college',
	'aspc.housing',
	'aspc.minutes',
	'aspc.eatshop',
	'aspc.events',
	'aspc.activityfeed',
	'aspc.courses',
	'aspc.menu',
	'aspc.files',
	'aspc.mentalhealth',
	'aspc.forum'
)

# Serializer to use for User sessions. Preferable not to use
# pickle, but existing code depends on serializing more sophisticated
# Python types than JSON can support
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
		},
	},
	'filters': {
		 'require_debug_false': {
			 '()': 'django.utils.log.RequireDebugFalse'
		 }
	 },
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		},
		'console':{
			'level':'DEBUG',
			'class':'logging.StreamHandler',
			'formatter': 'simple'
		},
		'logfile': {
			'level':'DEBUG',
			'class':'logging.handlers.RotatingFileHandler',
			'filename': PROJECT_ROOT + '/../log/django.log',
			'maxBytes': 50000,
			'backupCount': 2,
			'formatter': 'verbose',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
		'aspc': {
			'handlers': ['console', 'logfile'],
			'level': 'DEBUG',
		}
	}
}


# Django 1.7 requires a default test runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


LOGIN_REDIRECT_URL = '/'
WSGI_APPLICATION = "aspc.wsgi.application"

### Login Configuration
# See auth2 module
AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'aspc.auth2.backends.CASBackend', # Service to authenticate against the 5C CAS server
)

CAS_SETTINGS = {
	'SERVER_URL': 'https://ssocas.campus.pomona.edu/cas/',
	'ADMIN_PREFIX': 'admin'
}

#### Old Login Configuration (LDAP)
# See auth module
#
# LDAP Authentication information
#
#AUTHENTICATION_BACKENDS = (
#    'aspc.auth.backends.SimpleLDAPBackend',
#    'django.contrib.auth.backends.ModelBackend',
#)
#
#AUTH_LDAP = {
#    u'PO': {
#        'name': u"Pomona",
#        'server': u"ldap.pomona.edu",
#       'port': 389,
#        'bind_as': u'{0}@CAMPUS',
#       'filter': u'(cn={0})',
#        'base_dn': u"OU=Users and Computers,OU=ZHOME,DC=campus,DC=pomona,DC=edu",
#    },
#    # 'CMC': {
#    #     'name': "CMC",
#    #     'server': "ldap.pomona.edu",
#    #     'port': '389',
#    #     'bind_as': '{0}@CAMPUS',
#    #     'filter': '(cn={0})',
#    #     'base_dn': "OU=Student Accounts,OU=Users and Computers,OU=ZHOME,DC=campus,DC=pomona,DC=edu",
#    # },
#}
#
#AUTH_LDAP_DEFAULT_COLLEGE = "PO"
#
#AUTH_LDAP_COLLEGES = ((i[0], i[1]['name']) for i in AUTH_LDAP.items())




# Initial Data for Housing

DATA_ROOT = os.path.join(PROJECT_ROOT, 'housing', 'data')
DATA_PATHS = {
	'housing': {
		'buildings': os.path.join(DATA_ROOT, 'buildings.txt'),
		'rooms': os.path.join(DATA_ROOT, 'rooms.txt'),
		'suites': os.path.join(DATA_ROOT, 'suites.txt'),
		'maps': os.path.join(DATA_ROOT, 'maps.txt'),
		'maps_dir': os.path.join(DATA_ROOT, 'maps'),
	},
}

# Connection information for ITS Microsoft SQL Server
# (deployment-specific, overridden in settings.py)

COURSE_DATA_DB = {
	'HOST': '',
	'NAME': '',
	'USER': '',
	'PASSWORD': '',
}

#### Debug Toolbar Configuration

def show_toolbar(request):
	if request.user.is_superuser:
		return True
	else:
		return False

DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS': False,
	'SHOW_TOOLBAR_CALLBACK': 'aspc.configuration.show_toolbar',
}

# College Terms

ACADEMIC_TERM_DEFAULTS = {
  # Not the real start and end dates. Since those change year to year
  # this just provides defaults for prepopulating terms. Because of the way
  # current_term is calculated from these, it's better to have wider ranges.

  # Syntax:
  # term name: ((begin month, begin day), (end month, end day))

  'fall': ((8, 1), (12, 22)),
  'spring': ((1,10), (5, 25)),
}

#### Twitter Activity Feed Sources

TWITTER_FEEDS = ['pomonadining', 'SmithCampusCent', 'aspcsenate', 'pomonacollege']

# Menu API Authentication

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
}