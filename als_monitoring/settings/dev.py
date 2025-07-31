# dev on local.

from .base import *

SECRET_KEY = "django-insecure-!ac&lh-tyadp66m@$+a%&%pg@5*0lz596!*9%4+7m+m@=ns0kd"

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pgdb',
        'USER': 'chiemezuo',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

STATIC_URL = '/static/'
