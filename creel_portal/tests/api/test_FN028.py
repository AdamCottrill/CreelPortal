"""=============================================================
~/creel_portal/creel_portal/tests/api/test_FN028.py
 Created: 08 Apr 2020 12:53:49

 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN028 objects works as expected:

  + the fn028 list returns all of the fishing modes associated with a
  specific creel

  + the mode detail endpoint will return the mode code, mode
  description

 A. Cottrill
=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from creel_portal.models import FN028


from creel_portal.tests.pytest_fixtures import creel, api_client, user, user2


@pytest.mark.django_db
def test_fn028_list(api_client, creel):
    """the fn028 list returns all of the fishing modes associated with a
    specific creel.
    """

    prj_cd = creel.prj_cd

    url = reverse("creel_portal:api:fishing-mode-list", kwargs={"prj_cd": prj_cd})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [(x.get("mode"), x.get("mode_des")) for x in response.data["results"]]
    assert len(data) == 2

    expected = [("m1", "Mode 1"), ("m2", "Mode 2")]
    assert data == expected


@pytest.mark.django_db
def test_fn028_detail(api_client, creel):
    """ """

    prj_cd = creel.prj_cd
    mode = "m1"

    url = reverse(
        "creel_portal:api:fishing-mode-detail", kwargs={"prj_cd": prj_cd, "mode": mode}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "mode": "m1",
        "mode_des": "Mode 1",
    }

    for k, v in expected.items():
        assert response.data[k] == expected[k]
