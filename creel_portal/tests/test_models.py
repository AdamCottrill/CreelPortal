from django.test import TestCase
from creel_portal.models import *
from creel_portal.tests.factories import *


def test_lake_repr():
    """Verify that a lake is represented by object type, lake name and
    abbreviation."""
    lake = Lake(lake_name = 'Lake Huron', abbrev='HU')

    assert str(lake) == "<Lake: Lake Huron (HU)>"


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
