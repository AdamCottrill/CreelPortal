"""
=============================================================
~/creel_portal/tests/factories/fishnet_results.py
 Created: 03 Apr 2020 14:41:07

 DESCRIPTION:



 A. Cottrill
=============================================================
"""


import factory

from creel_portal.models.fishnet_results import (
    FR711,
    Strata,
    FR712,
    FR713,
    FR714,
    FR715,
)
from .common_factories import SpeciesFactory
from .fn011_factory import FN011Factory
from .creel_factories import (
    FN022Factory,
    FN023Factory,
    FN024Factory,
    FN026Factory,
    FN028Factory,
)


class FR711Factory(factory.DjangoModelFactory):
    """a factory for creel run settings and attributes"""

    class Meta:
        model = FR711
        django_get_or_create = ["creel", "run"]

    creel = factory.SubFactory(FN011Factory)
    run = factory.Sequence(lambda n: "{:02d}".format(n))
    strat_comb = "++_++_++_++"

    atycrit = 32
    cifopt = "12345"
    contmeth = "A2"
    do_cif = 1
    fr71_est = 2
    fr71_unit = 2
    mask_c = "++_++_++_++"
    save_daily = True


class StrataFactory(factory.DjangoModelFactory):
    """a factory for creel stratum - maps the FR712 objects to their
    assocaited entities in the design tables."""

    class Meta:
        model = Strata
        django_get_or_create = ["creel_run"]

    creel_run = factory.SubFactory(FR711Factory)

    season = factory.SubFactory(FN022Factory)
    daytype = factory.SubFactory(FN023Factory)
    period = factory.SubFactory(FN024Factory)
    area = factory.SubFactory(FN026Factory)
    mode = factory.SubFactory(FN028Factory)

    @factory.lazy_attribute
    def stratum_label(a):
        label = "{}_{}{}_{}_{}".format(
            a.season.ssn, a.daytype.dtp, a.period.prd, a.area.space, a.mode.mode
        )
        return label


class FR712Factory(factory.DjangoModelFactory):
    """a factory for creel strata attributes"""

    class Meta:
        model = FR712
        django_get_or_create = ["stratum"]

    stratum = factory.SubFactory(StrataFactory)
    rec_tp = 2
    strat_days = 11
    strat_hours = 77
    sam_days = 6
    sam_hours = 9.3
    fpc = 0.92
    prd_dur = 7
    atyunit = 2
    chkflag = 1
    strat_nn = 1


class FR713Factory(factory.DjangoModelFactory):
    """A factory for creel effort estimates.

    """

    class Meta:
        model = FR713
        django_get_or_create = ["fr712", "date"]

    fr712 = factory.SubFactory(FR712Factory)
    date = None

    person_s = 19
    cif_nn = 7
    effre_se = 0.0
    effae_se = 0.0
    effro_s = 102.34
    effao_s = 102.34
    tripne = 28.824
    aty_nn = 1
    aty1 = 0.0
    aty1_se = 0.0
    aty2 = 0.0
    aty2_se = 0.0
    angler_s = 19
    rod_s = 19


class FR714Factory(factory.DjangoModelFactory):
    """A factory for creel harvest estimates.

    """

    class Meta:
        model = FR714
        django_get_or_create = ["fr712"]

    fr712 = factory.SubFactory(FR712Factory)
    species = factory.SubFactory(SpeciesFactory)

    sek = True
    rod1_s = 20
    angler1_s = 20
    catno1_s = 1
    catno_s = 1
    cif1_nn = 11
    hvsno1_s = 1
    hvsno_s = 1
    mescnt_s = 0
    catne1 = 234.7
    catne1_se = 0.0
    catne = 234.7
    catne_se = 0.0
    effae1 = 421.4
    effae1_se = 0
    effao1_s = 102.34
    effpe1 = 156.14
    effre1 = 421.41
    effre1_se = 0.0
    effro1_s = 102.34
    hvscat_pc = 80.7
    hvsne = 189.41
    hvsne_se = 0
    hvsne1 = 189.41
    hvsne1_se = 0
    cuenao = 0.557
    cuenae = 0.557


class FR715Factory(factory.DjangoModelFactory):
    """A factory for angler option results.
    """

    class Meta:
        model = FR715
        django_get_or_create = ["fr712"]

    fr712 = factory.SubFactory(FR712Factory)

    ang_fn = "ANGGUID"
    ang_val = 1
    ang_freq = 21
    ang_prop = 0.875
    pty_freq = 8
    pty_prop = 0.889
