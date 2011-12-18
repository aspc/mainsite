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
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'django.contrib.redirects',
    'south',
    'folio',
    'senate',
    'blog',
    'auth',
    'sagelist',
    'college',
    'housing',
    'debug_toolbar',
    'minutes',
    'eatshop',
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
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

def show_toolbar(request):
    if request.user.is_superuser:
        return True
    else:
        return False

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}
