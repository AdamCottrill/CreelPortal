============
Creel Portal
============


Creel Portal is a Django application that provides an interface and
API for creels collected using the FN-II data model and analysed using
Creesys. It is built as an installable application.

Detailed documentation is in the "docs" directory.

Quick start
-----------

0. > pip install creel_portal.zip

1. Add creel_portal, django restframework, django_filter, and common and
   to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'django_filters',
        'common',        
        'creel_portal',
    ]

2. Include the creel_portal URLconf in your project urls.py like this::

    path('creel_portal/', include('creel_portal.urls')),

3. Run `python manage.py migrate` to create the creel_portal models.

4. Visit http://127.0.0.1:8000/creels or http://127.0.0.1:8000/creel_portal/api/v1


Updating the Application
------------------------


Rebuilding the App.
-------------------

Creel_portal was built as a standard applicaiton can be rebuild for
distrubition following the instructions found here:

https://docs.djangoproject.com/en/2.2/intro/reusable-apps/

With the creel_portal virtualenv active, and from within the
~/django_creel_portal directory, simply run:

> python setup.py sdist

The package will be placed in the ~/dist folder.  To install the
application run the command:

> pip install creel_portal.zip

To update an existing application issue the command:

> pip install --upgrade creel_portal.zip


Running the tests
------------------------

Creel_portal contains a number of unit tests that verify that the
application works as expected and that any regregressions are caught
early. The package uses pytest to run all of the tests, which can be
run by issuing the command:

> pytest

After the tests have completed, coverage reports can be found here:

~/htmlcov
