"""=============================================================
~/creel_portal/creel_portal/tests/api/test_temportal_strata.py
 Created: 08 Apr 2020 12:41:06


 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for the temporal strata works as expected.  This is a
  complex endpoint that integrates data and serializers for season,
  daytype, period, and exception dates.

 A. Cottrill
=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from creel_portal.tests.pytest_fixtures import creel, api_client, user, user2


@pytest.mark.django_db
def test_get_creel_temporal_strata(api_client, creel):
    """
    """

    assert 0 == 1
