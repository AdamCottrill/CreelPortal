from main.settings.base import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases


# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, '../db/db.sqlite3'),
#    }
# }
#

INSTALLED_APPS = INSTALLED_APPS + ["debug_toolbar", "django_extensions"]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# DATABASES = {
#    "default": {
#        #        'ENGINE': 'django.contrib.gis.db.backends.postgis',
#        #        'NAME': 'fisheye',
#        #        'USER': 'cottrillad',
#        #        'PASSWORD': 'django123',
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": os.path.join(BASE_DIR, "../db/creel_portal.db"),
#    }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "creel_portal",
        "USER": get_env_variable("PGUSER"),
        "PASSWORD": get_env_variable("PGPASSWORD"),
        "HOST": "localhost",
    }
}
