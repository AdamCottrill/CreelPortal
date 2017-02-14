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


class FN112Factory(factory.DjangoModelFactory):
    '''a factory for activity counts on creel logs'''

    class Meta:
        model = 'creel_portal.FN112'

    sama = factory.SubFactory(FN111Factory)

    atytm0 = datetime.strptime("06:15", "%H:%M").time()
    atytm1 = datetime.strptime("08:15", "%H:%M").time()
    atycnt = 10
    chkcnt = 8
    itvcnt = 3



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
    species = factory.SubFactory(Species)
    sek = True
    hvscnt = 3
    rlscnt = 1


class FN125Factory(factory.DjangoModelFactory):
    '''a factory for a sampled fish'''

    class Meta:
        model = 'creel_portal.FN125'

    catch = factory.SubFactory(FN123Factory)
    #species = factory.SubFactory(Species)

    grp = '10'
    fish = factory.Sequence(lambda n: '12{0}'.format(n))
    flen = 250
    tlen = 270



class FN127Factory(factory.DjangoModelFactory):
    '''A factory for age estimates for a particular fish.

    '''

    class Meta:
        model = 'creel_portal.FN127'

    fish = factory.SubFactory(FN125)
    ageid = factory.Sequence(lambda n: n)
    agea = 5
    agemt = ""
    conf = 7
    edge = '*'
    nca = 5


class FR713Factory(factory.DjangoModelFactory):
    '''A factory for creel effort estimates.

    '''

    class Meta:
        model = 'creel_portal.FR713'

    creel = factory.SubFactory(FN011)
    strat = '++_++_++_++'
    angler_s = 5
    aty_nn = 3
    chkcnt_s = 35
    cif_nn = 10
    itvcnt_s = 10
    person_s = 20
    rod_s = 10
    rod_ss = 25
    tripno = 0
    rec_tp = 2
    run = '01'


class FR714Factory(factory.DjangoModelFactory):
    '''A factory for creel harvest estimates.

    '''

    class Meta:
        model = 'creel_portal.FR714'

    creel = factory.SubFactory(FN011)
    species = factory.SubFactory(Species)

    strat = '++_++_++_++'

    sek = True
    rod1_s = 20
    angler1_s = 20
    catno1_s = 1
    catno_s = 1
    cif1_nn = 11
    hvsno1_s = 1
    hvsno_s = 1
    mescnt_s = 0
    rec_tp = 3
    run = '01'
