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

from creel_portal.models import FN011
from .user_factory import UserFactory
from .common_factories import LakeFactory


class FN011Factory(factory.DjangoModelFactory):
    """year and slug are built by the creel save method"""

    class Meta:
        model = FN011
        django_get_or_create = ["prj_cd"]

    prj_cd = "LHA_SC12_123"
    prj_nm = "Fake Creel"
    prj_ldr = factory.SubFactory(UserFactory)

    # prj_ldr = factory.SubFactory(UserFactory)
    comment0 = "This is a fake creel"

    contmeth = "A2"

    lake = factory.SubFactory(LakeFactory)

    @factory.lazy_attribute
    def prj_date0(a):
        datestring = "January 10, 20%s" % a.prj_cd[6:8]
        prj_date0 = datetime.strptime(datestring, "%B %d, %Y")
        return prj_date0

    @factory.lazy_attribute
    def prj_date1(a):
        datestring = "January 15, 20%s" % a.prj_cd[6:8]
        prj_date1 = datetime.strptime(datestring, "%B %d, %Y")
        return prj_date1

    @factory.post_generation
    def field_crew(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of field_crew were passed in, use them
            for crew in extracted:
                self.field_crew.add(crew)
