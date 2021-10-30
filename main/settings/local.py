from main.settings.base import *


INSTALLED_APPS = INSTALLED_APPS + ["debug_toolbar", "django_extensions"]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "creel_portal",
        "USER": get_env_variable("PGUSER"),
        "PASSWORD": get_env_variable("PGPASSWORD"),
        "HOST": "localhost",
    }
}
