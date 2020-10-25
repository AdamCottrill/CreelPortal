from main.settings.base import *

import os

# install gdal in virtualenv:
VIRTUAL_ENV = os.environ["VIRTUAL_ENV"].replace("(", "").replace(")", "")
OSGEO_VENV = os.path.join(VIRTUAL_ENV, "Lib/site-packages/osgeo")
GEOS_LIBRARY_PATH = os.path.join(OSGEO_VENV, "geos_c.dll")
GDAL_LIBRARY_PATH = os.path.join(OSGEO_VENV, "gdal300.dll")
os.environ["PATH"] += os.pathsep + str(OSGEO_VENV)


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
