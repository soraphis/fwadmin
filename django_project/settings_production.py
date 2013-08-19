from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fwadmin_db',
        'USER': 'fwadmin',
        'PASSWORD': open("db-password").read(),
        'HOST': 'localhost',
        'PORT': '',
    }
}
