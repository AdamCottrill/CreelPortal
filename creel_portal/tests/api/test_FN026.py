"""=============================================================
~/creel_portal/creel_portal/tests/api/test_FN026.py
 Created: 08 Apr 2020 12:53:49

 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN026 objects works as expected:

  + the fn026 list returns all of the spaces
  associated with a specific creel

  + the space detail endpoint will return the space code, space
  description, ddlat, ddlon.

 A. Cottrill
=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from creel_portal.models import FN026


from creel_portal.tests.pytest_fixtures import creel, api_client, user, user2


@pytest.mark.django_db
def test_fn026_list(api_client, creel):
    """ """

    prj_cd = creel.prj_cd

    url = reverse("creel_portal:api:space-list", kwargs={"prj_cd": prj_cd})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [
        (x.get("space"), x.get("space_des"), x.get("ddlat"), x.get("ddlon"))
        for x in response.data["results"]
    ]
    assert len(data) == 2

    expected = [("S1", "Space 1", 45.1, -81.1), ("S2", "Space 2", 45.2, -81.2)]
    assert data == expected


@pytest.mark.django_db
def test_fn026_detail(api_client, creel):
    """ """

    prj_cd = creel.prj_cd
    space = "S1"

    url = reverse(
        "creel_portal:api:space-detail", kwargs={"prj_cd": prj_cd, "space": space}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "space": "S1",
        "space_des": "Space 1",
        "ddlat": 45.1,
        "ddlon": -81.1,
    }

    for k, v in expected.items():
        assert response.data[k] == expected[k]
