from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG


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
