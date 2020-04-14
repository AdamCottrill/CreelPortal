import pytest
from django.core.exceptions import ValidationError

from datetime import datetime

from creel_portal.models.creel import FN025

from .factories.fishnet2_factories import FN011Factory
from .factories.creel_factories import (
    FN022Factory,
    FN023Factory,
    FN024Factory,
    FN025Factory,
    FN026Factory,
    FN028Factory,
    FN111Factory,
    FN112Factory,
)


@pytest.mark.django_db
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
    ssn = "22"
    creel = FN011Factory.build(prj_cd=prj_cd)
    season = FN022Factory.build(creel=creel, ssn=ssn)
    daytype = FN023Factory.build(season=season, dtp=dtp, dtp_nm=dtp_nm)

    shouldbe = "<DayType: {}({}) {}-{}>".format(dtp_nm, dtp, ssn, prj_cd)

    assert str(daytype) == shouldbe


@pytest.mark.django_db
def test_period_repr():
    """Verify that a period is represented by to prd code, the period
    start time, end time, the day type name it is associated with, the
    season name, and the project code and for the associated creel."""

    dtp = "2"
    dtp_nm = "Weekday"
    prj_cd = "LHA_SC11_123"
    ssn_des = "Summer"
    prd = "pm"
    prdtm0 = datetime.strptime("14:00", "%H:%M").time()
    prdtm1 = datetime.strptime("20:00", "%H:%M").time()

    creel = FN011Factory(prj_cd=prj_cd)
    season = FN022Factory(creel=creel, ssn_des=ssn_des)
    daytype = FN023Factory(season=season, dtp=dtp, dtp_nm=dtp_nm)
    period = FN024Factory(daytype=daytype, prd=prd, prdtm0=prdtm0, prdtm1=prdtm1)

    shouldbe = "<Period: {} ({}-{} ({} hrs)) {}-{}-{}>"
    start = prdtm0.strftime("%H:%M")
    end = prdtm1.strftime("%H:%M")
    prddur = "6.0"
    shouldbe = shouldbe.format(prd, start, end, prddur, dtp_nm, ssn_des, prj_cd)

    print("shouldbe={}".format(shouldbe))

    assert str(period) == shouldbe


def test_exception_dates_repr():
    """Verify that a exception dates are represented by object type,
    the date, the day type name, the season name,and the project code
    and for the associated creel."""

    dtp1 = "2"
    datestring = "2011-07-04"
    date = datetime.strptime(datestring, "%Y-%m-%d")
    prj_cd = "LHA_SC11_123"
    ssn_des = "Summer"

    creel = FN011Factory.build(prj_cd=prj_cd)
    season = FN022Factory.build(creel=creel, ssn_des=ssn_des)
    exceptiondate = FN025Factory.build(season=season, dtp1=dtp1, date=date)

    shouldbe = "<ExceptionDate: {} ({}-{})>".format(datestring, ssn_des, prj_cd)

    assert str(exceptiondate) == shouldbe


fn025_dates = [
    ["2017-10-15", "Date occurs before the associated season."],
    ["2017-12-15", "Date occurs after the associated season."],
]


@pytest.mark.django_db
@pytest.mark.parametrize("datestring,expected", fn025_dates)
def test_exception_date_clean(datestring, expected):
    """The FN025 model has a clean method that verifies that the exception
    date falls within the bounds of its associated season.  Verify
    that it works.

    """
    prj_cd = "LHA_SC11_123"
    ssn_date0 = datetime(2017, 11, 1)
    ssn_date1 = datetime(2017, 11, 30)
    # FN025_date = datetime(2017, 12, 10)
    FN025_date = datetime.strptime(datestring, "%Y-%m-%d")

    creel = FN011Factory(prj_cd=prj_cd)
    season = FN022Factory(creel=creel, ssn_date0=ssn_date0, ssn_date1=ssn_date1)
    fn025 = FN025(season=season, dtp1="1", date=FN025_date)

    with pytest.raises(ValidationError) as excinfo:
        fn025.save()

    # expected = "Date is not in the associated season."
    observed = excinfo.value.messages[0]

    assert expected == observed


def test_space_repr():
    """Verify that a spatial strata are represented by object type,
    the space description, the space code and the project code
    and for the associated creel."""

    prj_cd = "LHA_SC11_123"
    space = "AB"
    space_des = "the river"
    creel = FN011Factory.build(prj_cd=prj_cd)

    spatial_strata = FN026Factory.build(creel=creel, space=space, space_des=space_des)
    shouldbe = "<Space: {} ({}) [{}]>".format(space_des, space, prj_cd)

    assert str(spatial_strata) == shouldbe


def test_mode_repr():
    """Verify that a fishing mode is represented by object type,
    the mode description, the mode code and the project code
    and for the associated creel."""

    prj_cd = "LHA_SC11_123"
    mode = "AB"
    mode_des = "trolling"
    creel = FN011Factory.build(prj_cd=prj_cd)

    fishing_mode = FN028Factory.build(creel=creel, mode=mode, mode_des=mode_des)
    shouldbe = "<FishingMode: {} ({}) [{}]>".format(mode_des, mode, prj_cd)

    assert str(fishing_mode) == shouldbe


def test_sama_repr():
    """Verify that an interview log is represented by object type,
    the sama number, the straum code and the project code
    and for the associated creel."""

    prj_cd = "LHA_SC11_123"
    creel = FN011Factory.build(prj_cd=prj_cd)

    sama = "1230"
    interviewlog = FN111Factory.build(creel=creel, sama=sama)

    shouldbe = "<InterviewLog: {} ({})>".format(sama, prj_cd)

    assert str(interviewlog) == shouldbe


def test_sama_dow():
    """Verify that an interview log is represented by object type,
    the sama number, the straum code and the project code
    and for the associated creel."""

    prj_cd = "LHA_SC11_123"
    creel = FN011Factory.build(prj_cd=prj_cd)

    sama = "1230"

    datestr = "2017-02-05"  # Sunday
    interview_date = datetime.strptime(datestr, "%Y-%m-%d")
    interviewlog = FN111Factory.build(creel=creel, sama=sama, date=interview_date)
    assert interviewlog.dow == 1

    datestr = "2017-02-08"  # Wednesday
    interview_date = datetime.strptime(datestr, "%Y-%m-%d")
    interviewlog = FN111Factory.build(creel=creel, sama=sama, date=interview_date)
    assert interviewlog.dow == 4

    datestr = "2017-02-11"  # Saturday
    interview_date = datetime.strptime(datestr, "%Y-%m-%d")
    interviewlog = FN111Factory.build(creel=creel, sama=sama, date=interview_date)
    assert interviewlog.dow == 7


@pytest.mark.django_db
def test_sama_check_season():
    """Verify that the season method of a sama object returns the correct
    season."""

    prj_cd = "LHA_SC11_123"
    creel = FN011Factory(prj_cd=prj_cd)

    # APRIL
    ssnA_date0 = datetime.strptime("2014-04-01", "%Y-%m-%d")
    ssnA_date1 = datetime.strptime("2014-04-30", "%Y-%m-%d")
    ssnA = "AA"
    ssnA_des = "SeasonA"
    seasonA = FN022Factory(
        creel=creel,
        ssn=ssnA,
        ssn_des=ssnA_des,
        ssn_date0=ssnA_date0,
        ssn_date1=ssnA_date1,
    )

    daytype = FN023Factory(season=seasonA)
    periodA = FN024Factory(daytype=daytype)

    # MAY
    ssnB_date0 = datetime.strptime("2014-05-01", "%Y-%m-%d")
    ssnB_date1 = datetime.strptime("2014-05-30", "%Y-%m-%d")
    ssnB = "BB"
    ssnB_des = "SeasonB"
    seasonB = FN022Factory(
        creel=creel,
        ssn=ssnB,
        ssn_des=ssnB_des,
        ssn_date0=ssnB_date0,
        ssn_date1=ssnB_date1,
    )

    daytypeB = FN023Factory(season=seasonB)
    periodB = FN024Factory(daytype=daytypeB)

    # daytype = FN023Factory(season=seasonB)
    mydate = datetime.strptime("2014-04-15", "%Y-%m-%d")

    sama1 = FN111Factory(
        creel=creel, season=seasonA, daytype=daytype, date=mydate, period=periodA
    )
    assert sama1.check_season() is True

    # wrong season (may, date is April)
    sama2 = FN111Factory(
        creel=creel, season=seasonB, daytype=daytype, date=mydate, period=periodB
    )
    assert sama2.check_season() is False


@pytest.mark.django_db
def test_sama_check_daytype():
    """Given an interviewlog verify that the daytype matches the day type
    predicted by the date of the sam-log. The date used in this example
    will not be in the exceptions table.

    """

    prj_cd = "LHA_SC11_123"
    ssn = "22"
    creel = FN011Factory(prj_cd=prj_cd)
    ssn_date0 = datetime.strptime("2017-02-01", "%Y-%m-%d")
    ssn_date1 = datetime.strptime("2017-02-28", "%Y-%m-%d")
    season = FN022Factory(
        creel=creel, ssn=ssn, ssn_date0=ssn_date0, ssn_date1=ssn_date1
    )

    dtp1 = "1"
    dtp1_nm = "Weekend"
    dow_lst = "17"
    weekend = FN023Factory(season=season, dtp=dtp1, dtp_nm=dtp1_nm, dow_lst=dow_lst)

    dtp2 = "2"
    dtp2_nm = "Weekday"
    dow_lst = "23456"
    FN023Factory(season=season, dtp=dtp2, dtp_nm=dtp2_nm, dow_lst=dow_lst)

    period = FN024Factory(daytype=weekend)

    # A thursday between season start and end dates
    mydate = datetime.strptime("2017-02-09", "%Y-%m-%d")
    sama = FN111Factory(
        creel=creel, season=season, daytype=weekend, date=mydate, period=period
    )
    # this date was a thrusday and not a weekend
    assert sama.check_daytype() is False

    # a Saturday
    mydate = datetime.strptime("2017-02-12", "%Y-%m-%d")
    sama1 = FN111Factory(
        creel=creel, season=season, daytype=weekend, date=mydate, period=period
    )
    assert sama1.check_daytype() is True


@pytest.mark.django_db
def test_sama_check_daytype_exeption_date():
    """If an the date associated wth an iterview log occurs on an
    exception date, the check_daytype() method should return true if the
    daytype is a weekend (eventhough the event occured through the week)
    It will return false if the daytye is weekday and on a known exception
    date.

    """

    prj_cd = "LHA_SC11_123"
    ssn = "22"
    creel = FN011Factory(prj_cd=prj_cd)
    ssn_date0 = datetime.strptime("2017-02-01", "%Y-%m-%d")
    ssn_date1 = datetime.strptime("2017-02-28", "%Y-%m-%d")
    season = FN022Factory(
        creel=creel, ssn=ssn, ssn_date0=ssn_date0, ssn_date1=ssn_date1
    )

    dtp1 = "1"
    dtp1_nm = "Weekend"
    dow_lst = "17"
    weekend = FN023Factory(season=season, dtp=dtp1, dtp_nm=dtp1_nm, dow_lst=dow_lst)

    dtp2 = "2"
    dtp2_nm = "Weekday"
    dow_lst = "23456"
    weekday = FN023Factory(season=season, dtp=dtp2, dtp_nm=dtp2_nm, dow_lst=dow_lst)

    period = FN024Factory(daytype=weekend)

    # A thursday between season start and end dates
    mydate = datetime.strptime("2017-02-09", "%Y-%m-%d")

    # make my date an exceptino
    FN025Factory(season=season, dtp1=dtp1, date=mydate)

    sama = FN111Factory(
        creel=creel, season=season, daytype=weekday, date=mydate, period=period
    )
    # this date was a thrusday on the exception list and has the daytype correctly coded
    assert sama.check_daytype() is True
    assert sama.check_exception_date() is True

    # A thursday between season start and end dates
    mydate = datetime.strptime("2017-02-10", "%Y-%m-%d")

    sama2 = FN111Factory(
        creel=creel, season=season, daytype=weekday, date=mydate, period=period
    )
    # this date was a thrusday on the exception list and has the daytype correctly coded
    assert sama2.check_daytype() is True
    assert sama2.check_exception_date() is False


@pytest.mark.django_db
def test_sama_check_exception_date():
    """If the date of an interviewlog falls on a date in the exceptions
    table for that creel, the check_exception_date() method should
    return true, false otherwise.

    """

    prj_cd = "LHA_SC11_123"
    ssn = "22"
    creel = FN011Factory(prj_cd=prj_cd)
    ssn_date0 = datetime.strptime("2017-02-01", "%Y-%m-%d")
    ssn_date1 = datetime.strptime("2017-02-28", "%Y-%m-%d")
    season = FN022Factory(
        creel=creel, ssn=ssn, ssn_date0=ssn_date0, ssn_date1=ssn_date1
    )

    dtp = "2"
    dtp_nm = "Weekday"
    dow_lst = "23456"
    weekday = FN023Factory(season=season, dtp=dtp, dtp_nm=dtp_nm, dow_lst=dow_lst)

    period = FN024Factory(daytype=weekday)

    # A thursday between season start and end dates
    mydate = datetime.strptime("2017-02-09", "%Y-%m-%d")

    # make my date an exception
    FN025Factory(season=season, dtp1=dtp, date=mydate)

    sama1 = FN111Factory(
        creel=creel, season=season, daytype=weekday, date=mydate, period=period
    )
    assert sama1.check_exception_date() is True

    # the day before our exception date
    mydate2 = datetime.strptime("2017-02-08", "%Y-%m-%d")
    sama2 = FN111Factory(
        creel=creel, season=season, daytype=weekday, date=mydate2, period=period
    )
    assert sama2.check_exception_date() is False


@pytest.mark.django_db
def test_sama_check_period():
    """Given the date and time of an interview log, period should
    return the value of the associated period defined in the FN024
    table."""

    creel = FN011Factory()
    ssn_date0 = datetime.strptime("2017-04-01", "%Y-%m-%d")
    ssn_date1 = datetime.strptime("2017-04-30", "%Y-%m-%d")
    season = FN022Factory(creel=creel, ssn_date0=ssn_date0, ssn_date1=ssn_date1)
    daytype = FN023Factory(season=season)

    prd = "am"
    prdtm0 = datetime.strptime("08:00", "%H:%M").time()
    prdtm1 = datetime.strptime("12:00", "%H:%M").time()
    period = FN024Factory(daytype=daytype, prd=prd, prdtm0=prdtm0, prdtm1=prdtm1)

    prd = "noon"
    prdtm0 = datetime.strptime("12:00", "%H:%M").time()
    prdtm1 = datetime.strptime("16:00", "%H:%M").time()
    period2 = FN024Factory(daytype=daytype, prd=prd, prdtm0=prdtm0, prdtm1=prdtm1)

    prd = "pm"
    prdtm0 = datetime.strptime("16:00", "%H:%M").time()
    prdtm1 = datetime.strptime("20:00", "%H:%M").time()
    FN024Factory(daytype=daytype, prd=prd, prdtm0=prdtm0, prdtm1=prdtm1)

    # a day in the middle of our seasons
    mydate = datetime.strptime("2017-04-15", "%Y-%m-%d")
    mytime = datetime.strptime("14:00", "%H:%M").time()

    sama = FN111Factory(
        creel=creel,
        season=season,
        daytype=daytype,
        period=period,
        date=mydate,
        samtm0=mytime,
    )

    assert sama.check_period() is False

    sama2 = FN111Factory(
        creel=creel,
        season=season,
        daytype=daytype,
        period=period2,
        date=mydate,
        samtm0=mytime,
    )

    assert sama2.check_period() is True


@pytest.mark.django_db
def test_sama_stratum():
    '''given the space, mode, day type, period and season of an
    interview log, the stratum method should retuurn the FishNet-2
    stratum string of the form: "XX_XX_XX_XX."'''

    creel = FN011Factory()

    ssn = "SN"
    ssn_date0 = datetime.strptime("2017-04-01", "%Y-%m-%d")
    ssn_date1 = datetime.strptime("2017-04-30", "%Y-%m-%d")
    season = FN022Factory(
        creel=creel, ssn=ssn, ssn_date0=ssn_date0, ssn_date1=ssn_date1
    )
    dtp = "2"
    daytype = FN023Factory(season=season, dtp="2")

    prd = "2"
    prdtm0 = datetime.strptime("12:00", "%H:%M").time()
    prdtm1 = datetime.strptime("16:00", "%H:%M").time()
    period = FN024Factory(daytype=daytype, prd=prd, prdtm0=prdtm0, prdtm1=prdtm1)

    space = "SP"
    spatial_strata = FN026Factory(creel=creel, space=space)

    mode = "AB"
    fishing_mode = FN028Factory(creel=creel, mode=mode)

    # a day in the middle of our seasons
    mydate = datetime.strptime("2017-04-15", "%Y-%m-%d")
    # a time in the middle of our period
    mytime = datetime.strptime("14:00", "%H:%M").time()

    sama = FN111Factory.build(
        creel=creel,
        season=season,
        daytype=daytype,
        period=period,
        date=mydate,
        samtm0=mytime,
        area=spatial_strata,
        mode=fishing_mode,
    )

    shouldbe = "{}_{}{}_{}_{}".format(ssn, dtp, prd, space, mode)

    assert sama.stratum == shouldbe


def test_creel_activity_count_repr():
    """Verify that at interview counts (FN112 objects) are represented by
    object type, project code, the sama number, start time, and end
    time

    """

    prj_cd = "LHA_SC11_123"
    creel = FN011Factory.build(prj_cd=prj_cd)

    sama = "1230"
    interviewlog = FN111Factory.build(creel=creel, sama=sama)

    time0_str = "14:00"
    time1_str = "16:00"
    time0 = datetime.strptime(time0_str, "%H:%M").time()
    time1 = datetime.strptime(time1_str, "%H:%M").time()

    interview_counts = FN112Factory.build(sama=interviewlog, atytm0=time0, atytm1=time1)

    shouldbe = "ActivityCount: {}-{} {}-{}".format(prj_cd, sama, time0, time1)
    assert str(interview_counts) == shouldbe
