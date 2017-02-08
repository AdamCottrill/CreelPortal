import factory
from datetime import datetime
from django.template.defaultfilters import slugify

from creel_portal.models import *


class LakeFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'creel_portal.Lake'

    lake_name = "Lake Huron"
    abbrev = "HU"

class FN011Factory(factory.DjangoModelFactory):
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
        prj_date0 = datetime.strptime(datestring, "%B %d, %Y")
        return(prj_date0)

    @factory.lazy_attribute
    def prj_date1(a):
        datestring = "January 15, 20%s" % a.prj_cd[6:8]
        prj_date1 = datetime.strptime(datestring, "%B %d, %Y")
        return(prj_date1)


class FN022Factory(factory.DjangoModelFactory):
    '''a factory for seasons'''

    class Meta:
        model = 'creel_portal.FN022'

    creel = factory.SubFactory(FN011Factory)
    ssn = "01"
    ssn_des = "Spring"

    @factory.lazy_attribute
    def ssn_date0(a):
        datestring = "April 15, 2015"
        ssn_date0 = datetime.strptime(datestring, "%B %d, %Y")
        return(ssn_date0)

    @factory.lazy_attribute
    def ssn_date1(a):
        datestring = "June 15, 2015"
        ssn_date1 = datetime.strptime(datestring, "%B %d, %Y")
        return(ssn_date1)


class FN023Factory(factory.DjangoModelFactory):
    '''a factory for daytypes'''

    class Meta:
        model = 'creel_portal.FN023'

    dow_lst = "17"
    dtp = "1"
    dtp_nm = "Weekend"
    season = factory.SubFactory(FN022Factory)


class FN024Factory(factory.DjangoModelFactory):
    '''a factory for daily periods (am/pm)'''

    class Meta:
        model = 'creel_portal.FN024'

    daytype = factory.SubFactory(FN023Factory)
    prd = "am"
    prdtm0 = datetime.strptime("06:00", "%H:%M").time()
    prdtm1 = datetime.strptime("13:00", "%H:%M").time()
