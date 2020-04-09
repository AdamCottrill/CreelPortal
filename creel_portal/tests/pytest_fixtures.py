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

from datetime import datetime, time

from .factories.user_factory import UserFactory
from .factories.fn011_factory import FN011Factory
from .factories.creel_factories import (
    FN022Factory,
    FN023Factory,
    FN024Factory,
    FN025Factory,
    FN026Factory,
    FN028Factory,
)
from .factories.fishnet_results import FR711Factory, StrataFactory


SCOPE = "function"


@pytest.fixture(scope=SCOPE)
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture(scope=SCOPE)
def user(db):
    """return a normal user named homer
    """
    password = "Abcd1234"
    homer = UserFactory.create(
        username="hsimpson",
        first_name="Homer",
        last_name="Simpson",
        password=password,
        email="homer@simpsons.com",
    )
    homer.set_password(password)
    homer.save()
    return homer


@pytest.fixture(scope=SCOPE)
def user2(db):
    password = "Abcd1234"
    user2 = UserFactory(
        username="gcostanza",
        first_name="George",
        last_name="Costanza",
        email="george@nbc.com",
        password=password,
    )
    user2.set_password(password)
    user2.save()
    return user2


@pytest.fixture(scope=SCOPE)
def creels(user, user2):

    creel1 = FN011Factory(prj_ldr=user, prj_cd="LHA_SC19_001", prj_nm="First Creel")
    creel2 = FN011Factory(prj_ldr=user, prj_cd="LHA_SC19_002", prj_nm="Second Creel")
    creel3 = FN011Factory(prj_ldr=user2, prj_cd="LHA_SC19_003", prj_nm="Third Creel")

    return [creel1, creel2, creel3]


@pytest.fixture(scope=SCOPE)
def creel(db, user, user2):
    """a fixture to setup to relatively complicated state of a single
    creel - this fixture returns a creel object with two seasons, two
    daytypes and two periods (one per datetype).  It has a single
    exception date, two spaces and two fishing modes.

    """

    prj_cd = "LHA_SC17_123"

    ssn = "12"
    ssn_des = "February"
    creel = FN011Factory(prj_cd=prj_cd, prj_ldr=user, field_crew=[user2,])
    ssn_date0 = datetime.strptime("2017-02-01", "%Y-%m-%d")
    ssn_date1 = datetime.strptime("2017-02-28", "%Y-%m-%d")
    season = FN022Factory(
        creel=creel, ssn=ssn, ssn_des=ssn_des, ssn_date0=ssn_date0, ssn_date1=ssn_date1
    )

    ssn = "13"
    ssn_des = "March"
    creel = FN011Factory(prj_cd=prj_cd)
    ssn_date0 = datetime.strptime("2017-03-01", "%Y-%m-%d")
    ssn_date1 = datetime.strptime("2017-03-31", "%Y-%m-%d")
    season2 = FN022Factory(
        creel=creel, ssn=ssn, ssn_des=ssn_des, ssn_date0=ssn_date0, ssn_date1=ssn_date1
    )

    dtp1 = "1"
    dtp1_nm = "Weekend"
    dow_lst = "17"
    weekend = FN023Factory(season=season, dtp=dtp1, dtp_nm=dtp1_nm, dow_lst=dow_lst)
    weekend2 = FN023Factory(season=season2, dtp=dtp1, dtp_nm=dtp1_nm, dow_lst=dow_lst)

    dtp2 = "2"
    dtp2_nm = "Weekday"
    dow_lst = "23456"
    weekday = FN023Factory(season=season, dtp=dtp2, dtp_nm=dtp2_nm, dow_lst=dow_lst)
    weekday2 = FN023Factory(season=season2, dtp=dtp2, dtp_nm=dtp2_nm, dow_lst=dow_lst)

    prd_am = 1
    prdtm0_am = time(6, 0)
    prdtm1_am = time(12, 0)
    prd_dur_am = 6

    prd_pm = 2
    prdtm0_pm = time(12, 0)
    prdtm1_pm = time(20, 0)
    prd_dur_pm = 8

    # February weekend mornings and afternoons
    FN024Factory(
        daytype=weekend,
        prd=prd_am,
        prdtm0=prdtm0_am,
        prdtm1=prdtm1_am,
        prd_dur=prd_dur_am,
    )
    FN024Factory(
        daytype=weekend,
        prd=prd_pm,
        prdtm0=prdtm0_pm,
        prdtm1=prdtm1_pm,
        prd_dur=prd_dur_pm,
    )
    # February week day mornings and afternoons
    FN024Factory(
        daytype=weekday,
        prd=prd_am,
        prdtm0=prdtm0_am,
        prdtm1=prdtm1_am,
        prd_dur=prd_dur_am,
    )
    FN024Factory(
        daytype=weekday,
        prd=prd_pm,
        prdtm0=prdtm0_pm,
        prdtm1=prdtm1_pm,
        prd_dur=prd_dur_pm,
    )

    # March weekend mornings and afternoons
    FN024Factory(
        daytype=weekend2,
        prd=prd_am,
        prdtm0=prdtm0_am,
        prdtm1=prdtm1_am,
        prd_dur=prd_dur_am,
    )
    FN024Factory(
        daytype=weekday2,
        prd=prd_pm,
        prdtm0=prdtm0_pm,
        prdtm1=prdtm1_pm,
        prd_dur=prd_dur_pm,
    )
    # March week day mornings and afternoons
    FN024Factory(
        daytype=weekday2,
        prd=prd_am,
        prdtm0=prdtm0_am,
        prdtm1=prdtm1_am,
        prd_dur=prd_dur_am,
    )
    FN024Factory(
        daytype=weekend2,
        prd=prd_pm,
        prdtm0=prdtm0_pm,
        prdtm1=prdtm1_pm,
        prd_dur=prd_dur_pm,
    )

    FN025Factory(
        season=season,
        date=datetime.strptime("2017-02-16", "%Y-%m-%d"),
        dtp1="1",
        description="Family Day",
    )

    FN026Factory(creel=creel, space="S1", space_des="Space 1", ddlat=45.1, ddlon=-81.1)
    FN026Factory(creel=creel, space="S2", space_des="Space 2", ddlat=45.2, ddlon=-81.2)
    FN028Factory(creel=creel, mode="m1", mode_des="Mode 1")
    FN028Factory(creel=creel, mode="m2", mode_des="Mode 2")

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
