"""
=============================================================

~/creel_portal/tests/factories/fn011_factory.py
 Created: 03 Apr 2020 09:55:22

 DESCRIPTION:

  Factories for objects presenting the tables in the Fishnet2 data model:

    + FN011


 A. Cottrill
=============================================================
"""

import factory

from datetime import datetime

from creel_portal.models.fishnet2 import FN011
from .user_factory import UserFactory
from .common_factories import LakeFactory


class FN011Factory(factory.DjangoModelFactory):
    """year and slug are built by the creel save method"""

    class Meta:
        model = FN011
        django_get_or_create = [
            "prj_cd",
        ]

    prj_cd = "LHA_SC12_123"
    prj_nm = "Fake Creel"
    prj_ldr = factory.SubFactory(UserFactory)
    # prj_ldr = factory.SubFactory(UserFactory)
    comment0 = "This is a fake creel"

    lake = factory.SubFactory(LakeFactory)

    @factory.lazy_attribute
    def prj_date0(a):
        datestring = "January 15, 20%s" % a.prj_cd[6:8]
        prj_date0 = datetime.strptime(datestring, "%B %d, %Y")
        return prj_date0

    @factory.lazy_attribute
    def prj_date1(a):
        datestring = "January 15, 20%s" % a.prj_cd[6:8]
        prj_date1 = datetime.strptime(datestring, "%B %d, %Y")
        return prj_date1
