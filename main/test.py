# usage: python manage.py test pjtk2 --settings=main.test_settings
# flake8: noqa
"""Settings to be used for running tests."""
import logging
import os

from main.settings import *

#USE_TZ = False

#INSTALLED_APPS += ('django_nose',)
#INSTALLED_APPS.append('django_jasmine')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)



##logging.getLogger("factory").setLevel(logging.WARN)
