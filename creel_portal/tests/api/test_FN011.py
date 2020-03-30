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


def test_fn011_list():
    """
    """
    assert 0 == 1
