from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

FWADMIN_REALLY_SEND_MAIL = True
FWADMIN_REAL_LDAP = True

from ldap_auto_discover.ldap_auto_discover import ldap_auto_discover
AUTH_LDAP_SERVER_URI = lambda: ldap_auto_discover("uni-trier.de")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fwadmin_db',
        'USER': 'fwadmin',
        'PASSWORD': open(os.path.join(
            os.path.dirname(__file__), "db-password")).read(),
        'HOST': 'localhost',
        'PORT': '',
    }
}
