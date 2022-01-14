"""=============================================================
~/creel_portal/creel_portal/tests/api/test_FN024.py
 Created: 08 Apr 2020 12:41:06


 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN024 objects works as expected:

  + the fn024 list returns all of the periods for a daytype
  associated with a specific season

  + the period detail endpoint will return the period label, the start
  time, end time, and period duration

 A. Cottrill
=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from creel_portal.models import FN024


from creel_portal.tests.pytest_fixtures import creel, api_client, user, user2


@pytest.mark.django_db
def test_fn024_list(api_client, creel):
    """the fn024 list will return all of the periods for a daytype
    associated with a specific season.
    """

    prj_cd = creel.prj_cd
    ssn = "12"
    dtp = 1  # weekend

    url = reverse(
        "creel_portal:api:period-list", kwargs={"prj_cd": prj_cd, "ssn": ssn, "dtp": 1}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [
        (x.get("prd"), x.get("prdtm0"), x.get("prdtm1"))
        for x in response.data["results"]
    ]
    assert len(data) == 2

    expected = [("1", "06:00:00", "12:00:00"), ("2", "12:00:00", "20:00:00")]
    assert data == expected


@pytest.mark.django_db
def test_fn024_detail(api_client, creel):
    """the period detail endpoint will return the period label, the start
    time, end time, and period duration
    """

    prj_cd = creel.prj_cd
    ssn = "12"
    dtp = 1
    prd = 1

    url = reverse(
        "creel_portal:api:period-detail",
        kwargs={"prj_cd": prj_cd, "ssn": ssn, "dtp": dtp, "prd": prd},
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {"prd": "1", "prdtm0": "06:00:00", "prdtm1": "12:00:00", "prd_dur": 6.0}

    for k, v in expected.items():
        assert response.data[k] == expected[k]
