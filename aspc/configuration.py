import os, django

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

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
#submitting requests with a fake HTTP Host header, which is possible even 
# under many seemingly-safe web server configurations.
ALLOW_HOSTS = [
    '.aspc.pomona.edu',
    '.aspc.pomona.edu.', # allow FQDN (with trailing dot)
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static'),
)

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
    "aspc.context_processors.site",
    "aspc.context_processors.absolute_uri",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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
    'grappelli.dashboard', # Must be before grappelli
    'grappelli', # Must be before django.contrib.admin
    'filebrowser', # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'django.contrib.redirects',
    'django.contrib.humanize',
    'gunicorn',
    'south',
    'django_extensions',
    'debug_toolbar',
    'djcelery',
    'kombu.transport.django',
    'stdimage',
    'aspc.folio',
    'aspc.senate',
    'aspc.blog',
    'aspc.auth',
    'aspc.sagelist',
    'aspc.college',
    'aspc.housing',
    'aspc.coursesearch',
    'aspc.minutes',
    'aspc.eatshop',
    'aspc.events',
    'aspc.activityfeed',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'aspc': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

LOGIN_REDIRECT_URL = '/'

#### ASPC Specific Configuration

# LDAP Authentication information

AUTHENTICATION_BACKENDS = (
    'aspc.auth.backends.SimpleLDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP = {
    'PO': {
        'name': "Pomona",
        'server': "ldap.pomona.edu",
        'port': '389',
        'bind_as': '{0}@CAMPUS',
        'filter': '(cn={0})',
        'base_dn': "OU=Users and Computers,OU=ZHOME,DC=campus,DC=pomona,DC=edu",
    },
    # 'CMC': {
    #     'name': "CMC",
    #     'server': "ldap.pomona.edu",
    #     'port': '389',
    #     'bind_as': '{0}@CAMPUS',
    #     'filter': '(cn={0})',
    #     'base_dn': "OU=Student Accounts,OU=Users and Computers,OU=ZHOME,DC=campus,DC=pomona,DC=edu",
    # },
}

AUTH_LDAP_DEFAULT_COLLEGE = "PO"

AUTH_LDAP_COLLEGES = ((i[0], i[1]['name']) for i in AUTH_LDAP.items())

# Initial Data for Housing

DATA_ROOT = os.path.join(PROJECT_ROOT, '..', 'data')
DATA_PATHS = {
    'housing': {
        'buildings': os.path.join(DATA_ROOT, 'housing', 'buildings.txt'),
        'rooms': os.path.join(DATA_ROOT, 'housing', 'rooms.txt'),
        'suites': os.path.join(DATA_ROOT, 'housing', 'suites.txt'),
        'maps': os.path.join(DATA_ROOT, 'housing', 'maps.txt'),
        'maps_dir': os.path.join(DATA_ROOT, 'housing', 'maps'),
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

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
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

#### Celery Configuration
import djcelery

BROKER_URL = "django://"
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

djcelery.setup_loader()

#### Grappelli Configuration

GRAPPELLI_INDEX_DASHBOARD = 'aspc.dashboard.CustomIndexDashboard'
GRAPPELLI_ADMIN_TITLE = 'Associated Students of Pomona College'

#### Twitter Activity Feed Sources

TWITTER_FEEDS = ['pomonadining', 'SmithCampusCent', 'aspcsenate', 'pomonacollege']
