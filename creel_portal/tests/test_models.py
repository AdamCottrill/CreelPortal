
from creel_portal.models import *
from creel_portal.tests.factories import *

import pytest


def test_lake_repr():
    """Verify that a lake is represented by object type, lake name and
    abbreviation."""
    lake = Lake(lake_name='Lake Huron', abbrev='HU')

    assert str(lake) == "<Lake: Lake Huron (HU)>"


def test_species_repr():
    """the string method for species objects should return the object type
    (Species), the common_name, and if available, the scientific name
    in brackets.

    """

    common_name = "Gold Fish"
    scientific_name = 'fishicus goldicus'

    spc1 = SpeciesFactory.build(common_name=common_name,
                                scientific_name=scientific_name)

    spc2 = SpeciesFactory.build(common_name=common_name,
                                scientific_name=None)

    assert str(spc1) == '<Species: {} ({})>'.format(common_name,
                                                    scientific_name)

    assert str(spc2) == '<Species: {}>'.format(common_name)


def test_creel_repr():
    """Verify that a creel is represented by object type, creel name and
    project code."""

    prj_nm = "Test Creel"
    prj_cd = "LHA_SC11_123"

    creel = FN011Factory.build(prj_nm=prj_nm, prj_cd=prj_cd)

    shouldbe = "<Creel: {} ({})>".format(prj_nm, prj_cd)

    assert str(creel) == shouldbe


def test_season_repr():
    """Verify that a sesaon is represented by object type, season description,
    season code, project code and for the associated creel."""

    ssn = "11"
    ssn_des = "Summer Vacation"
    prj_cd = "LHA_SC11_123"

    creel = FN011Factory.build(prj_cd=prj_cd)
    season = FN022Factory.build(creel=creel, ssn=ssn, ssn_des=ssn_des)

    shouldbe = "<Season: {} ({}) [{}]>".format(ssn_des, ssn, prj_cd)

    assert str(season) == shouldbe


def test_daytype_repr():
    """Verify that a daytype is represented by object type, the day type name,
    the day type code and  the project code and for the associated creel."""

    dtp = "2"
    dtp_nm = "Weekday"
    prj_cd = "LHA_SC11_123"
    ssn = '22'
    creel = FN011Factory.build(prj_cd=prj_cd)
    season = FN022Factory.build(creel=creel, ssn=ssn)
    daytype = FN023Factory.build(season=season, dtp=dtp, dtp_nm=dtp_nm)

    shouldbe = "<DayType: {}({}) {}-{}>".format(dtp_nm, dtp, ssn, prj_cd)

    assert str(daytype) == shouldbe


def test_period_repr():
    """Verify that a period is represented by to prd code, the period
    start time, end time, the day type name it is associated with, the
    season name, and the project code and for the associated creel."""

    dtp = "2"
    dtp_nm = "Weekday"
    prj_cd = "LHA_SC11_123"
    ssn_des = 'Summer'
    prd = 'pm'
    prdtm0 = datetime.strptime("14:00", "%H:%M").time()
    prdtm1 = datetime.strptime("20:00", "%H:%M").time()

    creel = FN011Factory.build(prj_cd=prj_cd)
    season = FN022Factory.build(creel=creel, ssn_des=ssn_des)
    daytype = FN023Factory.build(season=season, dtp=dtp, dtp_nm=dtp_nm)
    period = FN024Factory.build(daytype=daytype, prd=prd,
                                prdtm0=prdtm0, prdtm1=prdtm1)

    shouldbe = "<Period: {}({}-{}) {}-{}-{}>"
    start = prdtm0.strftime("%H:%M")
    end = prdtm1.strftime("%H:%M")
    shouldbe = shouldbe.format(prd, start, end, dtp_nm, ssn_des, prj_cd)

    assert str(period) == shouldbe


def test_exception_dates_repr():
    """Verify that a exception dates are represented by object type,
    the date, the day type name, the season name,and the project code
    and for the associated creel."""

    dtp1 = "2"
    datestring = '2011-07-04'
    date = datetime.strptime(datestring, '%Y-%m-%d')
    prj_cd = "LHA_SC11_123"
    ssn_des = 'Summer'

    creel = FN011Factory.build(prj_cd=prj_cd)
    season = FN022Factory.build(creel=creel, ssn_des=ssn_des)
    exceptiondate = FN025Factory.build(season=season, dtp1=dtp1, date=date)

    shouldbe = "<ExceptionDate: {} ({}-{})>".format(datestring,
                                                    ssn_des, prj_cd)

    assert str(exceptiondate) == shouldbe


def test_space_repr():
    """Verify that a spatial strata are represented by object type,
    the space description, the space code and the project code
    and for the associated creel."""

    prj_cd = "LHA_SC11_123"
    space = 'AB'
    space_des = 'the river'
    creel = FN011Factory.build(prj_cd=prj_cd)

    spatial_strata = FN026Factory.build(creel=creel, space=space,
                                        space_des=space_des)
    shouldbe = "<Space: {} ({}) [{}]>".format(space_des, space, prj_cd)

    assert str(spatial_strata) == shouldbe


def test_mode_repr():
    """Verify that a fishing mode is represented by object type,
    the mode description, the mode code and the project code
    and for the associated creel."""

    prj_cd = "LHA_SC11_123"
    mode = 'AB'
    mode_des = 'trolling'
    creel = FN011Factory.build(prj_cd=prj_cd)

    fishing_mode = FN028Factory.build(creel=creel, mode=mode,
                                      mode_des=mode_des)
    shouldbe = "<FishingMode: {} ({}) [{}]>".format(mode_des, mode, prj_cd)

    assert str(fishing_mode) == shouldbe


def test_sama_repr():
    """Verify that an interview log is represented by object type,
    the sama number, the straum code and the project code
    and for the associated creel."""

    prj_cd = "LHA_SC11_123"
    creel = FN011Factory.build(prj_cd=prj_cd)

    sama = '1230'
    interviewlog = FN111Factory.build(creel=creel, sama=sama)

    shouldbe = "<InterviewLog: {} ({})>".format(sama, prj_cd)

    assert str(interviewlog) == shouldbe


def test_sama_dow():
    """Verify that an interview log is represented by object type,
    the sama number, the straum code and the project code
    and for the associated creel."""

    prj_cd = "LHA_SC11_123"
    creel = FN011Factory.build(prj_cd=prj_cd)

    sama = '1230'

    datestr = '2017-02-05' #Sunday
    interview_date = datetime.strptime(datestr, '%Y-%m-%d')
    interviewlog = FN111Factory.build(creel=creel, sama=sama,
                                      date=interview_date)
    assert interviewlog.dow == 1

    datestr = '2017-02-08' #Wednesday
    interview_date = datetime.strptime(datestr, '%Y-%m-%d')
    interviewlog = FN111Factory.build(creel=creel, sama=sama,
                                      date=interview_date)
    assert interviewlog.dow == 4

    datestr = '2017-02-11' #Saturday
    interview_date = datetime.strptime(datestr, '%Y-%m-%d')
    interviewlog = FN111Factory.build(creel=creel, sama=sama,
                                      date=interview_date)
    assert interviewlog.dow == 7


@pytest.mark.django_db
def test_sama_season():
    """Verify that the season method of a sama object returns the correct
    season."""

    prj_cd = "LHA_SC11_123"
    creel = FN011Factory(prj_cd=prj_cd)

    ssnA_date0 = datetime.strptime('2014-04-01', '%Y-%m-%d')
    ssnA_date1 = datetime.strptime('2014-04-30', '%Y-%m-%d')
    ssnA = "AA"
    ssnA_des = 'SeasonA'
    seasonA = FN022Factory(creel=creel, ssn=ssnA, ssn_des=ssnA_des,
                           ssn_date0=ssnA_date0, ssn_date1=ssnA_date1)

    ssnB_date0 = datetime.strptime('2014-05-01', '%Y-%m-%d')
    ssnB_date1 = datetime.strptime('2014-05-30', '%Y-%m-%d')
    ssnB = "BB"
    ssnB_des = 'SeasonB'
    FN022Factory(creel=creel, ssn=ssnB, ssn_des=ssnB_des,
                 ssn_date0=ssnB_date0, ssn_date1=ssnB_date1)
    mydate = datetime.strptime('2014-05-15', '%Y-%m-%d')
    sama = FN111Factory.build(creel=creel, date=mydate)

    assert sama.season.ssn == ssnB
    assert sama.season.ssn_des == ssnB_des
    assert sama.season != seasonA


@pytest.mark.django_db
def test_sama_daytype():
    '''Given an interviewlog verify that it is able to return the correct
    daytype using the creel and date.  The date used in this example will
    not be in the exceptions table.'''

    prj_cd = "LHA_SC11_123"
    ssn = '22'
    creel = FN011Factory(prj_cd=prj_cd)
    ssn_date0 = datetime.strptime('2017-02-01', '%Y-%m-%d')
    ssn_date1 = datetime.strptime('2017-02-28', '%Y-%m-%d')
    season = FN022Factory(creel=creel, ssn=ssn, ssn_date0=ssn_date0,
                          ssn_date1=ssn_date1)

    dtp1 = "1"
    dtp1_nm = "Weekend"
    dow_lst = '17'
    FN023Factory(season=season, dtp=dtp1, dtp_nm=dtp1_nm, dow_lst=dow_lst)

    dtp2 = "2"
    dtp2_nm = "Weekday"
    dow_lst = '23456'
    FN023Factory(season=season, dtp=dtp2, dtp_nm=dtp2_nm, dow_lst=dow_lst)

    # A thursday between season start and end dates
    mydate = datetime.strptime('2017-02-09', '%Y-%m-%d')
    sama = FN111Factory.build(creel=creel, date=mydate)

    assert sama.daytype.dtp == dtp2
    assert sama.daytype.dtp_nm == dtp2_nm


@pytest.mark.django_db
def test_sama_daytype_exception():
    '''If the date of an interviewlog falls on a date in the exceptions
    table for that creel, the day type in the exceptions table should be
    returned regardless of which day of the week the interview
    occurred.'''

    prj_cd = "LHA_SC11_123"
    ssn = '22'
    creel = FN011Factory(prj_cd=prj_cd)
    ssn_date0 = datetime.strptime('2017-02-01', '%Y-%m-%d')
    ssn_date1 = datetime.strptime('2017-02-28', '%Y-%m-%d')
    season = FN022Factory(creel=creel, ssn=ssn, ssn_date0=ssn_date0,
                          ssn_date1=ssn_date1)

    dtp1 = "1"
    dtp1_nm = "Weekend"
    dow_lst = '17'
    FN023Factory(season=season, dtp=dtp1, dtp_nm=dtp1_nm, dow_lst=dow_lst)

    dtp2 = "2"
    dtp2_nm = "Weekday"
    dow_lst = '23456'
    FN023Factory(season=season, dtp=dtp2, dtp_nm=dtp2_nm, dow_lst=dow_lst)

    # A thursday between season start and end dates
    mydate = datetime.strptime('2017-02-09', '%Y-%m-%d')

    # make my date an exception
    FN025Factory(season=season, dtp1=dtp1, date=mydate)

    sama = FN111Factory.build(creel=creel, date=mydate)

    assert sama.daytype.dtp == dtp1
    assert sama.daytype.dtp_nm == dtp1_nm


@pytest.mark.django_db
def test_sama_period():
    '''Given the date and time of an interview log, period should
    return the value of the associated period defined in the FN024
    table.'''

    creel = FN011Factory()
    ssn_date0 = datetime.strptime('2017-04-01', '%Y-%m-%d')
    ssn_date1 = datetime.strptime('2017-04-30', '%Y-%m-%d')
    season = FN022Factory(creel=creel, ssn_date0=ssn_date0,
                          ssn_date1=ssn_date1)
    daytype = FN023Factory(season=season)

    prd = 'am'
    prdtm0 = datetime.strptime("08:00", "%H:%M").time()
    prdtm1 = datetime.strptime("12:00", "%H:%M").time()
    FN024Factory(daytype=daytype, prd=prd, prdtm0=prdtm0, prdtm1=prdtm1)

    prd = 'noon'
    prdtm0 = datetime.strptime("12:00", "%H:%M").time()
    prdtm1 = datetime.strptime("16:00", "%H:%M").time()
    period2 = FN024Factory(daytype=daytype, prd=prd,
                           prdtm0=prdtm0, prdtm1=prdtm1)

    prd = 'pm'
    prdtm0 = datetime.strptime("16:00", "%H:%M").time()
    prdtm1 = datetime.strptime("20:00", "%H:%M").time()
    FN024Factory(daytype=daytype, prd=prd, prdtm0=prdtm0, prdtm1=prdtm1)

    #a day in the middle of our seasons
    mydate = datetime.strptime('2017-04-15', '%Y-%m-%d')
    mytime = datetime.strptime("14:00", "%H:%M").time()

    sama = FN111Factory.build(creel=creel, date=mydate, samtm0=mytime)

    assert sama.period == period2


@pytest.mark.django_db
def test_sama_stratum():
    '''given the space, mode, day type, period and season of an
    interview log, the stratum method should retuurn the FishNet-2
    stratum string of the form: "XX_XX_XX_XX."'''

    creel = FN011Factory()

    ssn = "SN"
    ssn_date0 = datetime.strptime('2017-04-01', '%Y-%m-%d')
    ssn_date1 = datetime.strptime('2017-04-30', '%Y-%m-%d')
    season = FN022Factory(creel=creel, ssn=ssn, ssn_date0=ssn_date0,
                          ssn_date1=ssn_date1)
    dtp = '2'
    daytype = FN023Factory(season=season, dtp='2')

    prd = '2'
    prdtm0 = datetime.strptime("12:00", "%H:%M").time()
    prdtm1 = datetime.strptime("16:00", "%H:%M").time()
    FN024Factory(daytype=daytype, prd=prd, prdtm0=prdtm0, prdtm1=prdtm1)

    space = 'SP'
    spatial_strata = FN026Factory(creel=creel, space=space)

    mode = 'AB'
    fishing_mode = FN028Factory(creel=creel, mode=mode)

    # a day in the middle of our seasons
    mydate = datetime.strptime('2017-04-15', '%Y-%m-%d')
    # a time in the middle of our period
    mytime = datetime.strptime("14:00", "%H:%M").time()

    sama = FN111Factory.build(creel=creel, date=mydate, samtm0=mytime,
                              area=spatial_strata, mode=fishing_mode)

    shouldbe = '{}_{}{}_{}_{}'.format(ssn, dtp, prd, space, mode)

    assert sama.stratum == shouldbe


def test_sam_repr():
    """The string method of a creel interview should return the object
    type (an interveiw), the sample number and the project code."""

    sam_num = '12345'
    prj_cd = "LHA_SC11_123"
    creel = FN011Factory.build(prj_cd=prj_cd)
    sam = FN121Factory.build(creel=creel, sam=sam_num)

    assert str(sam) == '<Interview: {} ({})>'.format(sam_num, prj_cd)


def test_catch_count_repr():
    """The string method of a catch count should return the object
    type (a catch count), project code, the sample, species code."""

    spc = '091'
    sam_num = '12345'
    prj_cd = "LHA_SC11_123"
    species = SpeciesFactory.build(species_code=spc)
    creel = FN011Factory.build(prj_cd=prj_cd)
    interview = FN121Factory.build(creel=creel, sam=sam_num)
    catch = FN123Factory.build(interview=interview, species=species)

    assert str(catch) == '<Catch: {}-{}-{}>'.format(prj_cd, sam_num, spc)


def test_fish_repr():
    """The string method of fish should return the object
    type (fish), project code, the sample, species code, group code
    and fish number."""

    spc = '091'
    sam_num = '12345'
    prj_cd = "LHA_SC11_123"
    grp = '55'
    fish_num = 321

    species = SpeciesFactory.build(species_code=spc)
    creel = FN011Factory.build(prj_cd=prj_cd)
    interview = FN121Factory.build(creel=creel, sam=sam_num)
    catch = FN123Factory.build(interview=interview, species=species)
    fish = FN125Factory.build(catch=catch, grp=grp,
                              fish=fish_num)

    shouldbe = '<Fish: {}-{}-{}-{}-{}>'.format(prj_cd, sam_num, spc,
                                               grp, fish_num)
    assert str(fish) == shouldbe
