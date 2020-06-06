# usage: python manage.py test pjtk2 --settings=main.test_settings
# flake8: noqa
"""Settings to be used for running tests."""

from main.settings.base import *


SECRET_KEY = "testing"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "creel_portal",
        "USER": get_env_variable("PGUSER"),
        "PASSWORD": get_env_variable("PGPASSWORD"),
        "HOST": "localhost",
    }
}

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)


COVERAGE_MODULE_EXCLUDES = ["migrations", "fixtures", "admin$", "utils", "config"]
COVERAGE_MODULE_EXCLUDES += THIRD_PARTY_APPS + DJANGO_APPS
# COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(__file__, '../../../coverage')
#
