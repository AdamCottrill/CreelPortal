"""
=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/creel_portal/creel_portal/tests/factories/common_factories.py
 Created: 02 Apr 2020 10:45:20


 DESCRIPTION:

  Factories for objects imported from the uglmu common application.

 A. Cottrill
=============================================================
"""


import factory

from common.models import Lake, Species


class SpeciesFactory(factory.DjangoModelFactory):
    class Meta:
        model = Species
        django_get_or_create = ("spc",)

    # species_code = '81'
    spc = factory.Sequence(lambda n: n)
    spc_nmco = "Lake Trout"
    spc_nmsc = "Salvelinus nameychush"


class LakeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Lake
        django_get_or_create = ("abbrev",)

    lake_name = "Lake Huron"
    abbrev = "HU"
