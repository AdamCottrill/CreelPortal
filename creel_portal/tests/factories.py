import factory
from datetime import datetime
from django.template.defaultfilters import slugify

from creel_portal.models import *


class SpeciesFactory(factory.DjangoModelFactory):
    class Meta:
        model = Species
    #species_code = '81'
    species_code = factory.Sequence(lambda n: n)
    common_name = 'Lake Trout'
    scientific_name = 'Salvelinus nameychush'

class LakeFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'creel_portal.Lake'

    lake_name = "Lake Huron"
    #abbrev = "HU"
    abbrev = factory.Sequence(lambda n: 'H{0}'.format(n))

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


class FN025Factory(factory.DjangoModelFactory):
    '''a factory for daytype exeptions (holidays)'''

    class Meta:
        model = 'creel_portal.FN025'

    date = datetime.strptime("2015-07-01", "%Y-%m-%d")
    dtp1 = "1"
    season = factory.SubFactory(FN022Factory)


class FN026Factory(factory.DjangoModelFactory):
    '''a factory for spatial strata'''

    class Meta:
        model = 'creel_portal.FN026'

    space = "01"
    space_des = "The Lake"
    creel = factory.SubFactory(FN011Factory)


class FN028Factory(factory.DjangoModelFactory):
    '''a factory for fishing modes'''

    class Meta:
        model = 'creel_portal.FN028'

    mode = "01"
    mode_des = "Ice Fishing"
    creel = factory.SubFactory(FN011Factory)
    atyunit = 1
    itvunit = 1
    chkflag = 0

class FN111Factory(factory.DjangoModelFactory):
    '''a factory for fishing modes'''

    class Meta:
        model = 'creel_portal.FN111'

    creel = factory.SubFactory(FN011Factory)
    area = factory.SubFactory(FN026Factory)
    mode = factory.SubFactory(FN028Factory)

    date = datetime.strptime("2015-07-01", "%Y-%m-%d")
    samtm0 = datetime.strptime("06:15", "%H:%M").time()



class FN121Factory(factory.DjangoModelFactory):
    '''a factory for creel interviews'''

    class Meta:
        model = 'creel_portal.FN121'

    creel = factory.SubFactory(FN011Factory)
    area = factory.SubFactory(FN026Factory)
    mode = factory.SubFactory(FN028Factory)
    sama = factory.SubFactory(FN111Factory)

    itvseq = factory.Sequence(lambda n: '{0}'.format(n))
    sam = factory.Sequence(lambda n: '235{0}'.format(n))
    date = datetime.strptime("2015-07-01", "%Y-%m-%d")
    itvtm0 = datetime.strptime("08:15", "%H:%M").time()
    efftm0 = datetime.strptime("06:15", "%H:%M").time()
    effcmp = False


class FN123Factory(factory.DjangoModelFactory):
    '''a factory for catch counts by species for an interview'''

    class Meta:
        model = 'creel_portal.FN123'

    interview = factory.SubFactory(FN121Factory)
    sek = True
    hvscnt = 3
    rlscnt = 1
