"""=============================================================
~/creel_portal/creel_portal/tests/api/test_FN025.py
 Created: 08 Apr 2020 12:41:06


 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN025 objects works as expected:

  + the fn025 list returns the exception dates assocaited with a
  season within a creel.

  + the exception date detail endpoint will return the exception date,
  the daytype code (dtp1), and description.

+ creations rules:

  + date must occur after season start and before season endpoint
  + cannot already exist in the season
  + should not be a weekend (they are already exceptional)


 A. Cottrill
=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from creel_portal.models import FN025


from creel_portal.tests.pytest_fixtures import creel, api_client, user, user2


@pytest.mark.django_db
def test_fn025_list(api_client, creel):
    """the fn025 list will return all of the periods for a daytype
    associated with a specific season.
    """

    prj_cd = creel.prj_cd
    ssn = "12"

    url = reverse(
        "creel_portal:api:exception-date-list", kwargs={"prj_cd": prj_cd, "ssn": ssn}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [
        (x.get("date"), x.get("dtp1"), x.get("description"))
        for x in response.data["results"]
    ]
    assert len(data) == 1

    expected = [("2017-02-16", "1", "Family Day")]
    assert data == expected


@pytest.mark.django_db
def test_fn025_detail(api_client, creel):
    """ """

    prj_cd = creel.prj_cd
    ssn = "12"

    url = reverse(
        "creel_portal:api:exception-date-detail",
        kwargs={"prj_cd": prj_cd, "ssn": ssn, "date": "2017-02-16"},
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {"date": "2017-02-16", "dtp1": "1", "description": "Family Day"}

    for k, v in expected.items():
        assert response.data[k] == expected[k]
