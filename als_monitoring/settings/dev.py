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

    # Temporary SQLite config for data dump
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}

STATIC_URL = '/static/'
