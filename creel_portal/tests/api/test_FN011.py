"""=============================================================
~/creel_portal/creel_portal/tests/api/test_FN011.py
 Created: 29 Mar 2020 17:21:32

 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN011 objects works as expected:


+ creel-list should be available to both logged in and anonomous users

+ creel-list be filterable for year, lake, creel type, first year,
last year, and project lead

+ creel detail should contains the proper elements:

+ post, put and delete endpoint should only be available to admin or
project lead users, they should not be available for anaoous users, or
field crew (who cannot edit or create projects)

 A. Cottrill
=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from creel_portal.models import FN011

from fixtures import api_client, user, user2, creels
from creel_portal.tests.pytest_fixtures import creel


@pytest.mark.django_db
def test_fn011_list(api_client, creels):
    """
    """
    url = reverse("creel-api:creel-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [x.get("prj_nm") for x in response.data["results"]]
    assert len(data) == 3

    expected = ["First Creel", "Second Creel", "Third Creel"]
    for x in expected:
        assert x in data


@pytest.mark.django_db
def test_fn011_detail(api_client, creel):
    """The creel detail endpoint should return all of the relavent details for a creel:

    + lake
    + prj_cd
    + prj_nm
    + prj_ldr
    + prj_date0
    + prj_date1
    + cont_meth

    """

    assert 0 == 1
