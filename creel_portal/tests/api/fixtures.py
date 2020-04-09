# """=============================================================
# ~/creel_portal/tests/api/fixtures.py
#  Created: 08 Apr 2020 10:46:00

#  DESCRIPTION:

#   A number of fixtures that will be used in testing the api endpoints
#   for creel portal

#  A. Cottrill
# =============================================================

# """


# import pytest

# from creel_portal.tests.factories.fishnet2_factories import FN011Factory
# from creel_portal.tests.factories.user_factory import UserFactory


# @pytest.fixture
# def api_client():
#     from rest_framework.test import APIClient

#     return APIClient()


# @pytest.fixture
# def user():
#     user = UserFactory(username="hsimpson")
#     user.set_password("Abcd1234")
#     user.save()
#     return user


# @pytest.fixture
# def user2():
#     user2 = UserFactory(username="gcostanza")
#     user2.set_password("Abcd1234")
#     user2.save()
#     return user2


# @pytest.fixture
# def creels(user, user2):

#     creel1 = FN011Factory(prj_ldr=user, prj_cd="LHA_SC19_001", prj_nm="First Creel")
#     creel2 = FN011Factory(prj_ldr=user, prj_cd="LHA_SC19_002", prj_nm="Second Creel")
#     creel3 = FN011Factory(prj_ldr=user2, prj_cd="LHA_SC19_003", prj_nm="Third Creel")

#     return [creel1, creel2, creel3]
