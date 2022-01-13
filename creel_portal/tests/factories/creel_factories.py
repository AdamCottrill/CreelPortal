"""
=============================================================
~/creel_portal/creel_portal/tests/factories/creel_design_factories.py
 Created: 02 Apr 2020 13:44:43

 DESCRIPTION:



 A. Cottrill
=============================================================
"""

import pytest
import factory

from datetime import datetime

from .fn011_factory import FN011Factory
from creel_portal.models import (
    FN022,
    FN023,
    FN024,
    FN025,
    FN026,
    FN028,
    FN111,
    FN112,
)


class FN022Factory(factory.DjangoModelFactory):
    """a factory for seasons"""

    class Meta:
        model = FN022
        django_get_or_create = ["creel", "ssn"]

    creel = factory.SubFactory(FN011Factory)
    ssn = "01"
    ssn_des = "Spring"

    @factory.lazy_attribute
    def ssn_date0(a):
        datestring = "April 15, 2015"
        ssn_date0 = datetime.strptime(datestring, "%B %d, %Y")
        return ssn_date0

    @factory.lazy_attribute
    def ssn_date1(a):
        datestring = "June 15, 2015"
        ssn_date1 = datetime.strptime(datestring, "%B %d, %Y")
        return ssn_date1


class FN023Factory(factory.DjangoModelFactory):
    """a factory for daytypes"""

    class Meta:
        model = FN023
        django_get_or_create = ["season", "dtp"]

    dow_lst = "17"
    dtp = "1"
    dtp_nm = "Weekend"
    season = factory.SubFactory(FN022Factory)


class FN024Factory(factory.DjangoModelFactory):
    """a factory for daily periods (am/pm)"""

    class Meta:
        model = FN024
        django_get_or_create = ["daytype", "prd"]

    daytype = factory.SubFactory(FN023Factory)
    prd = "am"
    prdtm0 = datetime.strptime("06:00", "%H:%M").time()
    prdtm1 = datetime.strptime("13:00", "%H:%M").time()


class FN025Factory(factory.DjangoModelFactory):
    """a factory for daytype exeptions (holidays)"""

    class Meta:
        model = FN025
        django_get_or_create = ["season", "date"]

    date = datetime.strptime("2015-07-01", "%Y-%m-%d")
    dtp1 = "1"
    season = factory.SubFactory(FN022Factory)


class FN026Factory(factory.DjangoModelFactory):
    """a factory for spatial strata"""

    class Meta:
        model = FN026
        django_get_or_create = ["creel", "space"]

    space = "01"
    space_des = "The Lake"
    creel = factory.SubFactory(FN011Factory)


class FN028Factory(factory.DjangoModelFactory):
    """a factory for fishing modes"""

    class Meta:
        model = FN028
        django_get_or_create = ["creel", "mode"]

    mode = "01"
    mode_des = "Ice Fishing"
    creel = factory.SubFactory(FN011Factory)
    atyunit = 1
    itvunit = 1
    chkflag = 0


class FN111Factory(factory.DjangoModelFactory):
    """a factory for fishing modes"""

    class Meta:
        model = FN111

    sama = factory.Sequence(lambda n: "%d" % n)

    creel = factory.SubFactory(FN011Factory)
    season = factory.SubFactory(FN022Factory)
    daytype = factory.SubFactory(FN023Factory)
    period = factory.SubFactory(FN024Factory)
    area = factory.SubFactory(FN026Factory)
    mode = factory.SubFactory(FN028Factory)

    date = datetime.strptime("2015-07-01", "%Y-%m-%d")
    samtm0 = datetime.strptime("06:15", "%H:%M").time()


class FN112Factory(factory.DjangoModelFactory):
    """a factory for activity counts on creel logs"""

    class Meta:
        model = FN112

    sama = factory.SubFactory(FN111Factory)

    atytm0 = datetime.strptime("06:15", "%H:%M").time()
    atytm1 = datetime.strptime("08:15", "%H:%M").time()
    atycnt = 10
    chkcnt = 8
    itvcnt = 3
