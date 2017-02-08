import factory
from datetime import datetime
from django.template.defaultfilters import slugify

from creel_portal.models import *


class LakeFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'creel_portal.Lake'

    lake_name = "Lake Huron"
    abbrev = "HU"

class FN011(factory.DjangoModelFactory):
    '''year and slug are built by the creel save method'''

    class Meta:
        model = 'creel_portal.FN011'

    prj_cd = "LHA_SC12_123"
    prj_nm = "Fake Creel"
    prj_ldr = "Bob Sakamano"
    #prj_ldr = factory.SubFactory(UserFactory)
    comment0 = "This is a fake creel"

    lake = factory.SubFactory(LakeFactory)

    @factory.lazy_attribute
    def prj_date0(a):
        datestring = "January 15, 20%s" % a.prj_cd[6:8]
        prj_date0 = datetime.datetime.strptime(datestring, "%B %d, %Y")
        return(prj_date0)

    @factory.lazy_attribute
    def prj_date1(a):
        datestring = "January 15, 20%s" % a.prj_cd[6:8]
        prj_date1 = datetime.datetime.strptime(datestring, "%B %d, %Y")
        return(prj_date1)
