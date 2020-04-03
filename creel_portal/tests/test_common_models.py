"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/creel_portal/creel_portal/tests/test_common_models.py
 Created: 02 Apr 2020 10:48:38


 DESCRIPTION:

Unit tests for the objects from the common django application - make
sure we can access and use them.

 A. Cottrill
=============================================================

"""


# from creel_portal.models import *
from .factories.common_factories import LakeFactory, SpeciesFactory
from .factories.user_factory import UserFactory

import pytest


@pytest.mark.django_db
def test_user_repr():
    """Make sure that our user objects are being created and represented
    the way we think they should be.

    """
    email = "barneyg@simspons"
    myuser = UserFactory(first_name="Barney", last_name="Gumble", email=email)

    assert str(myuser) == email
    assert myuser.username == "gumbleba"


def test_lake_repr():
    """Verify that a lake is represented by object type, lake name and
    abbreviation."""
    lake = LakeFactory.build(lake_name="Lake Huron", abbrev="HU")

    assert str(lake) == "Lake Huron (HU)"


def test_lake_repr():
    """Verify that a lake is represented by object type, lake name and
    abbreviation."""
    lake = LakeFactory.build(lake_name="Lake Huron", abbrev="HU")

    assert str(lake) == "Lake Huron (HU)"


def test_species_repr():
    """the string method for species objects should return the object type
    (Species), the spc_nmco, and if available, the scientific name
    in brackets.

    """

    spc_nmco = "Gold Fish"
    spc = "111"

    spc1 = SpeciesFactory.build(spc_nmco=spc_nmco, spc=spc)

    assert str(spc1) == "{} ({})".format(spc_nmco, spc)
