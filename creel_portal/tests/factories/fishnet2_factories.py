"""
=============================================================
~/creel_portal/creel_portal/tests/factories/common_factories.py
 Created: 02 Apr 2020 12:35:24

 DESCRIPTION:

  Factories for objects presenting the tables in the Fishnet2 data model:

    + FN011
    + FN121
    + FN123
    + FN125
    + FN125_Tags
    + FN125_Lamprey
    + FN127


 A. Cottrill
=============================================================
"""

import factory

from datetime import datetime

from creel_portal.models.fishnet2 import (
    FN121,
    FN123,
    FN125,
    FN125_Tag,
    FN125_Lamprey,
    FN127,
)

from .fn011_factory import FN011Factory
from .creel_factories import FN026Factory, FN028Factory, FN111Factory
from .common_factories import SpeciesFactory


class FN121Factory(factory.DjangoModelFactory):
    """a factory for creel interviews"""

    class Meta:
        model = FN121
        django_get_or_create = ["sama", "sam"]

    # creel = factory.SubFactory(FN011Factory)
    # area = factory.SubFactory(FN026Factory)
    # mode = factory.SubFactory(FN028Factory)
    sama = factory.SubFactory(FN111Factory)

    itvseq = factory.Sequence(lambda n: "{0}".format(n))
    sam = factory.Sequence(lambda n: "235{0}".format(n))
    date = datetime.strptime("2015-07-01", "%Y-%m-%d")
    itvtm0 = datetime.strptime("08:15", "%H:%M").time()
    efftm0 = datetime.strptime("06:15", "%H:%M").time()
    effcmp = False


class FN123Factory(factory.DjangoModelFactory):
    """a factory for catch counts by species for an interview"""

    class Meta:
        model = FN123
        django_get_or_create = ["interview", "grp", "species"]

    interview = factory.SubFactory(FN121Factory)
    species = factory.SubFactory(SpeciesFactory)
    grp = "00"
    sek = True
    hvscnt = 3
    rlscnt = 1


class FN125Factory(factory.DjangoModelFactory):
    """a factory for a sampled fish"""

    class Meta:
        model = FN125
        django_get_or_create = ["catch", "fish"]

    catch = factory.SubFactory(FN123Factory)

    fish = factory.Sequence(lambda n: "12{0}".format(n))
    flen = 250
    tlen = 270


class FN125TagFactory(factory.DjangoModelFactory):
    """A factory for tags associated wtih a fish

    """

    class Meta:
        model = FN125_Tag
        django_get_or_create = ["fish", "fish_tag_id"]

    fish = factory.SubFactory(FN125)
    fish_tag_id = factory.Sequence(lambda n: n)
    tagid = "12345"
    tagdoc = "25025"
    tagstat = "C"


class FN125LampreyFactory(factory.DjangoModelFactory):
    """A factory for Lamprey Wounds associated wtih a fish

    """

    class Meta:
        model = FN125_Lamprey
        django_get_or_create = ["fish", "lamid"]

    fish = factory.SubFactory(FN125)
    lamid = factory.Sequence(lambda n: n)
    lamijc = "A125"
    lamijc_type = "A1"
    lamijc_type = 25


class FN127Factory(factory.DjangoModelFactory):
    """A factory for age estimates for a particular fish.

    """

    class Meta:
        model = FN127
        django_get_or_create = ["fish", "ageid"]

    fish = factory.SubFactory(FN125)
    ageid = factory.Sequence(lambda n: n)
    agea = 5
    agemt = ""
    conf = 7
    edge = "*"
    nca = 5
