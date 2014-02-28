# Django settings for django_project project.
import ldap
import os
from django_auth_ldap.config import (
    LDAPSearch,
    ActiveDirectoryGroupType,
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

FWADMIN_REAL_LDAP = False

# XXX: can we do better? e.g. via socket.gethostbyname(me)
FWADMIN_HOST_URL_TEMPLATE = "https://fwadmin.uni-trier.de%(url)s"

# XXX: make all this part of a settings module in the DB?
FWADMIN_EMAIL_FROM="fwadmin@uni-trier.de"
FWADMIN_WARN_EXPIRE_DAYS=7

# the cisco access list number we use
FWADMIN_ACCESS_LIST_NR = 120
# the LDAP/django group that is allowed to use the tool 
FWADMIN_ALLOWED_USER_GROUP = "Mitarb"
# the LDAP/django group for the moderation
FWADMIN_MODERATORS_USER_GROUP = "G-zentrale-systeme"
# the default time a host is active if when created/renewed
FWADMIN_DEFAULT_ACTIVE_DAYS = 365
# mail about moderation requests
FWADMIN_MODERATION_WAITING_MAIL_NAG = "netz@uni-trier.de"

FWADMIN_REALLY_SEND_MAIL = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# XXX: make this more abstract to support multiple django apps(?)
LOGIN_URL = "/accounts/login/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fwadmin.db',                # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# auto gen a secret, submited to upstream django as
#  https://code.djangoproject.com/ticket/20181
_secrets_file = os.path.join(os.path.dirname(__file__), "secret.txt")
if os.path.exists(_secrets_file):
    with open(_secrets_file) as f:
        SECRET_KEY = f.read()

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'fwadmin.ctxprocessor.user_auth',
    'django.core.context_processors.i18n'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'django_project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'django_project.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), "..", "fwadmin", "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'bootstrapform',
    'south',
    'fwadmin',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(
                os.path.dirname(__file__), "..", "logs", "django.log"),
            'maxBytes': 500000,
            'backupCount': 10,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# LDAP/AD AUTH
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
)

# FUN! our active directory is setup so that we run into this:
#   https://bitbucket.org/psagers/django-auth-ldap/issue/21/cant-bind-and-search-on-activedirectory
# so we can not use something like
#   AUTH_LDAP_USER_DN_TEMPLATE = "%(user)s@emailtest.uni-trier.de"
# as the LDAP dn is set to the full user name, not to the SAMAccountName
#
if FWADMIN_REAL_LDAP:
    from ldap_auto_discover.ldap_auto_discover import ldap_auto_discover
    AUTH_LDAP_SERVER_URI = lambda: ldap_auto_discover("uni-trier.de")
AUTH_LDAP_BIND_DN = "testpm@uni-trier.de"
AUTH_LDAP_BIND_PASSWORD = open(os.path.join(os.path.dirname(__file__),
                                            "ldap-password")).read()


# custom search as the DN uses the full account name
AUTH_LDAP_USER_SEARCH = LDAPSearch('CN=Users,DC=uni-trier,DC=de', 
                                   ldap.SCOPE_SUBTREE, 
                                   '(CN=%(user)s)')

# needed to make ActiveDirectory work
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0
}

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName", 
    "last_name": "sn",
    "email": "maiL",
}
# this will crash and burn if there is no such group
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    # auto allow access to admin interface for our group
    "is_staff": "CN=G-zentrale-systeme,CN=Users,DC=uni-trier,DC=de",
}
# limit login to "Mitarb", (not needed, see fwadmin/view.py)
#AUTH_LDAP_REQUIRE_GROUP = "cn=Mitarb,CN=Users,dc=uni-trier,dc=de"
# have all the groups in the local django group database as well
AUTH_LDAP_MIRROR_GROUPS = True

AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType()
#AUTH_LDAP_CACHE_GROUPS = True
#AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600
AUTH_LDAP_GROUP_SEARCH = LDAPSearch('CN=Users,DC=uni-trier,DC=de',
                                    ldap.SCOPE_SUBTREE,
                                    "(objectClass=group)")

import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
)