"""
=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/creel_portal/creel_portal/tests/test_fishnet_results.py
 Created: 03 Apr 2020 14:46:49

 DESCRIPTION:



 A. Cottrill
=============================================================
"""


import pytest


from .pytest_fixtures import creel_run

from .factories.common_factories import SpeciesFactory
from .factories.fn011_factory import FN011Factory
from .factories.fishnet_results import (
    FR711Factory,
    FR712Factory,
    FR713Factory,
    FR714Factory,
    FR715Factory,
)


@pytest.mark.django_db
def test_fr711_repr():
    """Verify that the string representation of a creel run returns the
    project code and indicates the run number.  season code, project

    """

    prj_cd = "LHA_SC03_123"
    strat_comb = "??_+?_++_++"
    creel = FN011Factory(prj_cd=prj_cd)
    fr711 = FR711Factory(creel=creel, strat_comb=strat_comb)

    shouldbe = "{} (run:{} strat_comb:{})".format(prj_cd, fr711.run, strat_comb)

    assert str(fr711) == shouldbe


@pytest.mark.django_db
def test_fr712_repr(creel_run):
    """Verify that the string representation of a creel strata attributes
    object (FR712) returns the project code, the run number, the strata
    label, and the record type.

    """

    strata = creel_run.strata.first()

    prj_cd = creel_run.creel.prj_cd
    run = creel_run.run
    stratum_label = strata.stratum_label

    fr712 = FR712Factory(stratum=strata)

    shouldbe = "<Stratum Attributes: {}[{}] ({}, run:{}))>".format(
        stratum_label, fr712.rec_tp, prj_cd, run
    )

    assert str(fr712) == shouldbe


@pytest.mark.django_db
def test_fr713_repr(creel_run):
    """Verify that the string representation of a creel strata effort estimate
    object (FR713) returns the project code, the run number, the strata
    label, and the record type.

    """
    strata = creel_run.strata.first()

    fr712 = FR712Factory(stratum=strata)
    fr713 = FR713Factory(fr712=fr712)

    prj_cd = creel_run.creel.prj_cd
    run = creel_run.run
    stratum_label = strata.stratum_label

    shouldbe = "<Effort Estimate: {} (run:{} strat:{} rec_tp: {})>".format(
        prj_cd, run, stratum_label, fr712.rec_tp
    )

    assert str(fr713) == shouldbe


@pytest.mark.django_db
def test_fr714_repr(creel_run):
    """Verify that the string representation of a creel harvest/catch
    estimate object (FR714) returns the project code, the run number,
    the strata label, and the record type, species code, and whether
    or not the harvest was targetted or not.

    """

    strata = creel_run.strata.first()

    fr712 = FR712Factory(stratum=strata)

    spc = "075"
    sek = True
    species = SpeciesFactory(spc=spc)

    fr714 = FR714Factory(fr712=fr712, species=species, sek=sek)

    prj_cd = creel_run.creel.prj_cd
    run = creel_run.run
    stratum_label = strata.stratum_label

    shouldbe = "{}(run:{}): {}".format(prj_cd, run, stratum_label)

    shouldbe = "<HarvestEstimate: {}-{} sek:{} (prj_cd:{} run:{} rec_tp:{})>".format(
        stratum_label, spc, sek, prj_cd, run, fr712.rec_tp
    )

    assert str(fr714) == shouldbe


@pytest.mark.django_db
def test_fr715_repr(creel_run):
    """Verify that the string representation of a creel angler option
     object (FR715) returns the project code, the run number, the
     strata label, and the record type, angler option field name
     (ang_fn) and its associated value

    """

    strata = creel_run.strata.first()

    fr712 = FR712Factory(stratum=strata)
    fr715 = FR715Factory(fr712=fr712)

    prj_cd = creel_run.creel.prj_cd
    run = creel_run.run
    stratum_label = strata.stratum_label

    ang_fn = fr715.ang_fn
    ang_val = fr715.ang_val

    shouldbe = "<AnglerOption: {}={} ({} run:{} strat:{} rec_tp:{})>".format(
        ang_fn, ang_val, prj_cd, run, stratum_label, fr712.rec_tp
    )

    assert str(fr715) == shouldbe
