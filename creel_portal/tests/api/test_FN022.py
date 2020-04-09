"""=============================================================
~/creel_portal/creel_portal/tests/api/test_FN022.py
 Created: 08 Apr 2020 12:41:06


 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN022 objects works as expected:

  + the fn022 list returns all of the seasons associated with a
  specific creel

  + the season detail endpoint will return the ssn, ssn_des, start and
  end date

+ creation rules:

    + must occur before project start and before project endpoint
    + season must not overlap - each date can only belong to on season
    + there should not be any gaps - days that do not belong to a season.

 A. Cottrill
=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from creel_portal.models import FN022

from creel_portal.tests.pytest_fixtures import creel, user, user2, api_client


@pytest.mark.django_db
def test_fn022_list(api_client, creel):
    """
    """

    prj_cd = creel.prj_cd

    url = reverse("creel-api:season-list", kwargs={"prj_cd": prj_cd})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [(x.get("ssn"), x.get("ssn_des")) for x in response.data["results"]]
    assert len(data) == 2

    expected = [("12", "February"), ("13", "March")]
    assert data == expected


@pytest.mark.django_db
def test_fn022_detail(api_client, creel):
    """The season detail object should return 5 basic elements - the
    project code, season code, season description, start date and end
    date.
    """

    prj_cd = creel.prj_cd
    ssn = "12"

    url = reverse("creel-api:season-detail", kwargs={"prj_cd": prj_cd, "ssn": ssn})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "creel": prj_cd.lower(),
        "ssn": ssn,
        "ssn_des": "February",
        "ssn_date0": "2017-02-01",
        "ssn_date1": "2017-02-28",
    }

    for k, v in expected.items():
        assert response.data[k] == expected[k]
