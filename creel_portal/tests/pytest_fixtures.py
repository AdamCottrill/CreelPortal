"""=============================================================
~/creel_portal/tests/pytest_fixtures.py
 Created: 03 Apr 2020 10:45:01

 DESCRIPTION:

This file contains a number of fixtures or objects that are used by
our testing utilities.  The temporal components of creels are so
inter-related that difficult to rely on automatic factories.

 A. Cottrill
=============================================================

"""


import pytest

from datetime import datetime

from .factories.user_factory import UserFactory
from .factories.fn011_factory import FN011Factory
from .factories.creel_factories import (
    FN022Factory,
    FN023Factory,
    FN024Factory,
    FN026Factory,
    FN028Factory,
)
from .factories.fishnet_results import FR711Factory, StrataFactory


SCOPE = "function"


@pytest.fixture(scope=SCOPE)
def user(db):
    """return a normal user named homer
    """
    password = "Abcd1234"
    homer = UserFactory.create(
        username="hsimpson", first_name="Homer", last_name="Simpson", password=password
    )
    homer.save()
    return homer


@pytest.fixture(scope=SCOPE)
def creel(db):
    """a fixture to setup to relatively complicated state of a single
    creel - this fixture returns a creel object with a single season, two
    daytypes and two periods (one per datetype).
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

    FN024Factory(daytype=weekend)
    FN024Factory(daytype=weekday)

    return creel


@pytest.fixture(scope=SCOPE)
def creel_run(db):
    """a fixture to setup to relatively complicated state of a single
    creel including the creel run and strata objects.
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

    prd1 = FN024Factory(daytype=weekend, prd=1)
    FN024Factory(daytype=weekday, prd=2)

    space = FN026Factory(creel=creel, space="S1")
    mode = FN028Factory(creel=creel, mode="m1")

    creel_run = FR711Factory(creel=creel, run="01")
    StrataFactory(
        creel_run=creel_run,
        season=season,
        daytype=weekend,
        period=prd1,
        area=space,
        mode=mode,
    )

    return creel_run
