"""=============================================================
~/creel_portal/creel_portal/tests/api/test_FN023.py
 Created: 08 Apr 2020 12:41:06


 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN023 objects works as expected:

  + the fn023 list returns all of the daytypes associated with a
  specific season

  + the daytype detail endpoint will return the daytype code, the
  daytype name, and the dow_list

 A. Cottrill
=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from creel_portal.models import FN023

from fixtures import api_client
from creel_portal.tests.pytest_fixtures import creel


@pytest.mark.django_db
def test_fn023_list(api_client, creel):
    """The fn023 list endpoint should return all of the daytypes
    associated with a specific season.
    """

    prj_cd = creel.prj_cd
    ssn = "12"

    url = reverse("creel-api:day-type-list", kwargs={"prj_cd": prj_cd, "ssn": ssn})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [(x.get("dtp"), x.get("dtp_nm")) for x in response.data["results"]]
    assert len(data) == 2

    expected = [("1", "Weekend"), ("2", "Weekday")]
    assert data == expected


@pytest.mark.django_db
def test_fn023_detail(api_client, creel):
    """
    """

    assert 0 == 1
