"""=============================================================
~/creel_portal/creel_portal/tests/api/test_FN028.py
 Created: 08 Apr 2020 12:53:49

 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN028 objects works as expected:

  + the fn028 list returns all of the fishing modes associated with a
  specific creel

  + the space detail endpoint will return the space code, space
  description, ddlat, ddlon.

 A. Cottrill
=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from creel_portal.models import FN028

from fixtures import api_client
from creel_portal.tests.pytest_fixtures import creel


@pytest.mark.django_db
def test_fn028_list(api_client, creel):
    """the fn028 list returns all of the fishing modes associated with a
    specific creel.
    """

    prj_cd = creel.prj_cd

    url = reverse("creel-api:fishing-mode-list", kwargs={"prj_cd": prj_cd})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [(x.get("mode"), x.get("mode_des")) for x in response.data["results"]]
    assert len(data) == 2

    expected = [("m1", "Mode 1"), ("m2", "Mode 2")]
    assert data == expected


@pytest.mark.django_db
def test_fn028_detail(api_client, creel):
    """
    """

    assert 0 == 1
