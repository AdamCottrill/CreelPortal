"""
=============================================================
~/creel_portal/creel_portal/models/FishNetResults.py
 Created: 30 Mar 2020 08:39:05

 DESCRIPTION:

  This file contains all of the results tables from a fishnet-II project:

+ FR711
+ FR712
+ FR713
+ FR714
+ FR715

 A. Cottrill
=============================================================
"""


from django.db import models

from common.models import Species

from .FN011 import FN011
from .FN022 import FN022
from .FN023 import FN023
from .FN024 import FN024
from .FN026 import FN026
from .FN028 import FN028


from .choices import CONTMETH_CHOICES, REC_TP_CHOICES, ANG_FN_CHOICES


class Strata(models.Model):
    """A table that lies at the intersection of the design and data
    tables.  For new creels, we may want to add a build method that will
    create the stratum table using the cartesian product of all strata in
    the creel plus any defined in FR711
    """

    creel_run = models.ForeignKey(
        "FR711", related_name="strata", on_delete=models.CASCADE
    )

    stratum_label = models.CharField(max_length=11)

    # optional foreign keys:
    season = models.ForeignKey(
        FN022, related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    daytype = models.ForeignKey(
        FN023, related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    period = models.ForeignKey(
        FN024, related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    area = models.ForeignKey(
        FN026, related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    mode = models.ForeignKey(
        FN028, related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        app_label = "creel_portal"

        unique_together = ["creel_run", "stratum_label"]
        ordering = ["creel_run__creel__prj_cd", "creel_run__run", "stratum_label"]

    def __str__(self):
        """return the object type, the interview log number (sama), the stratum,
         and project code of the creel this record is assoicated
        with.

        """

        repr = "{}(run:{}): {}"
        return repr.format(
            self.creel_run.creel.prj_cd, self.creel_run.run, self.stratum_label
        )

    @property
    def strat_days(self):
        """Not sure if this should be a property or a field that this updated
        on save().

        Arguments:
        - `self`:
        """
        return self.calc_strat_days()

    @property
    def strat_hours(self):
        """Not sure if this should be a property or a field that this updated
        on save().

        Arguments:
        - `self`:

        """
        return self.calc_strat_hours()

    def calc_strat_days(self):
        """"""
        dtp = self.daytype.dtp
        days = self.season.get_strat_days(dtp)
        return days

    def calc_strat_hours(self):
        """"""
        days = self.calc_strat_days()
        prd_dir = self.period.prd_dur
        return days * prd_dir


class FR711(models.Model):
    """Class to hold creel strata settings.  this table contains
    information about contact method (access or roving creel), whether or
    not estimates are saved daily, and which strata can be combined or must
    be estimated separately (important for presenting final results as
    there may not be a ++_++_++_++ strata.

    """

    # CONTMETH_CHOICES = (
    #    ("A2", "Access; Same days"),
    #    ("R0", "Roving; No interviews"),
    #    ("R1", "Roving; Not same days"),
    #    ("R2", "Roving; Same days"),
    # )

    FR71_UNIT_CHOICES = ((0, "Rods"), (1, "Anglers"), (2, "Parties"))

    FR71_EST_CHOICES = ((1, "1-stage"), (2, "2-stage"))

    creel = models.ForeignKey(
        "FN011", related_name="creel_run", on_delete=models.CASCADE
    )
    run = models.CharField(max_length=2, default="01")

    atycrit = models.IntegerField()
    cifopt = models.CharField(max_length=5)
    contmeth = models.CharField(max_length=2, choices=CONTMETH_CHOICES, default="A2")
    do_cif = models.IntegerField()
    fr71_est = models.IntegerField(choices=FR71_EST_CHOICES)
    fr71_unit = models.IntegerField(choices=FR71_UNIT_CHOICES)
    mask_c = models.CharField(max_length=11, default="++_++_++_++")
    save_daily = models.BooleanField()
    strat_comb = models.CharField(max_length=11, default="++_++_++_++")

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FR711 - Effort Estimate"
        ordering = ["creel", "run"]
        unique_together = ["creel", "run"]

    def __str__(self):
        """return the object type (strata config), and the prj_cd,
        and the strat_comb.

        """
        repr = "{} (run:{} strat_comb:{})".format(
            self.creel.prj_cd, self.run, self.strat_comb
        )

        return repr


class FR712(models.Model):
    """This table contains all of the strata attributes - the number of
    day and hours in each strata, the number of days and hours sampled,
    and the period duration.

    NOTE: This table should probably be merged with Strata and Strata
    removed.

    """

    ATYUNIT_CHOICES = ((1, "Person"), (2, "Party"))

    CHKFLAG_CHOICES = ((0, "No"), (1, "Yes"))

    stratum = models.ForeignKey(
        Strata, on_delete=models.CASCADE, related_name="strata_attributes"
    )
    rec_tp = models.IntegerField(default=2, choices=REC_TP_CHOICES)
    strat_days = models.IntegerField()
    strat_hours = models.FloatField()
    sam_days = models.IntegerField(default=0, blank=True, null=True)
    sam_hours = models.FloatField(default=0, blank=True, null=True)
    fpc = models.FloatField(default=0, blank=True, null=True)
    prd_dur = models.FloatField()
    atyunit = models.IntegerField(
        default=2, choices=ATYUNIT_CHOICES, blank=True, null=True
    )
    chkflag = models.IntegerField(
        default=1, choices=CHKFLAG_CHOICES, blank=True, null=True
    )
    strat1 = models.CharField(blank=True, null=True, max_length=11)
    strat_nn = models.IntegerField(default=1)

    class Meta:
        app_label = "creel_portal"

    def __str__(self):
        """return the object type (stratum values), the stratum label, record
        type, the creel project code and run number

        """
        repr = "<Stratum Attributes: {}[{}] ({}, run:{}))>"
        return repr.format(
            self.stratum.stratum_label,
            self.rec_tp,
            self.stratum.creel_run.creel.prj_cd,
            self.stratum.creel_run.run,
        )


class FR713(models.Model):
    """Class to hold creel estimate of effort by strata.

    TODO - figure out if we need strat, if it should be build
    dynamically or ahead of time or if a '++' placeholder should be
    created add to each stratum of each creel to represent the
    collapsed 'all' estimate.

    """

    fr712 = models.ForeignKey(
        FR712, related_name="effort_estimates", on_delete=models.CASCADE
    )

    #    creel = models.ForeignKey(FN011, related_name='effort_estimates')
    #
    #    season = models.ForeignKey(FN022, related_name='effort_estimates',
    #                              blank=True, null=True)
    #    dtp = models.ForeignKey(FN023, related_name='effort_estimates',
    #                            blank=True, null=True)
    #    period = models.ForeignKey(FN024, related_name='effort_estimates',
    #                               blank=True, null=True)
    #    area = models.ForeignKey(FN026, related_name='effort_estimates',
    #                             blank=True, null=True)
    #    mode = models.ForeignKey(FN028, related_name='effort_estimates',
    #                             blank=True, null=True)
    #
    # TODO: run should be a fk to FR111 table
    # run = models.CharField(max_length=2, db_index=True)
    # rec_tp = models.IntegerField(default=2, choices=REC_TP_CHOICES)
    # strat = models.CharField(max_length=11)
    date = models.DateField(blank=True, null=True)

    chkcnt_s = models.IntegerField(blank=True, null=True)
    itvcnt_s = models.IntegerField(blank=True, null=True)
    person_s = models.IntegerField()

    cif_nn = models.IntegerField()

    effre = models.FloatField(blank=True, null=True)
    effre_se = models.FloatField()
    effre_vr = models.FloatField(blank=True, null=True)

    effae = models.FloatField(blank=True, null=True)
    effae_se = models.FloatField()
    effae_vr = models.FloatField(blank=True, null=True)

    effpe = models.FloatField(blank=True, null=True)
    effpe_se = models.FloatField(blank=True, null=True)
    effpe_vr = models.FloatField(blank=True, null=True)

    effro_s = models.FloatField()
    effro_ss = models.FloatField(blank=True, null=True)

    effpo_s = models.FloatField(blank=True, null=True)
    effpo_ss = models.FloatField(blank=True, null=True)

    effao_s = models.FloatField()
    effao_ss = models.IntegerField(blank=True, null=True)

    tripno = models.IntegerField(blank=True, null=True)
    tripne = models.FloatField()
    tripne_se = models.FloatField(blank=True, null=True)
    tripne_vr = models.FloatField(blank=True, null=True)

    aty_nn = models.IntegerField()
    aty_hrs = models.FloatField(blank=True, null=True)
    atycnt_s = models.IntegerField(blank=True, null=True)
    aty_days = models.IntegerField(blank=True, null=True)

    aty0 = models.FloatField(blank=True, null=True)

    aty1 = models.FloatField()
    aty1_se = models.FloatField()
    aty1_vr = models.FloatField(blank=True, null=True)

    aty2 = models.FloatField()
    aty2_se = models.FloatField()
    aty2_vr = models.FloatField(blank=True, null=True)

    angler_mn = models.FloatField(blank=True, null=True)
    angler_s = models.IntegerField()
    angler_ss = models.IntegerField(blank=True, null=True)

    rod_mna = models.FloatField(blank=True, null=True)
    rod_s = models.IntegerField()
    rod_ss = models.IntegerField(blank=True, null=True)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "EffortEstimate"
        unique_together = ["fr712", "date"]

    def __str__(self):
        """return the object type (EffortEstimate), and the prj_cd."""

        if self.date:
            repr = "<Effort Estimate: {} (run:{} strat:{} rec_tp: {} date:{})>"
            repr = repr.format(
                self.fr712.stratum.creel_run.creel.prj_cd,
                self.fr712.stratum.creel_run.run,
                self.fr712.stratum.stratum_label,
                self.fr712.rec_tp,
                self.date.strftime("%b-%d-%y"),
            )
        else:
            repr = "<Effort Estimate: {} (run:{} strat:{} rec_tp: {})>"
            repr = repr.format(
                self.fr712.stratum.creel_run.creel.prj_cd,
                self.fr712.stratum.creel_run.run,
                self.fr712.stratum.stratum_label,
                self.fr712.rec_tp,
            )
        return repr


class FR714(models.Model):
    """Class to hold creel estimate of harvest by strata and species.

    TODO - figure out if we need strat, if it should be build
    dynamically or ahead of time or if a '++' placeholder should be
    created add to each stratum of each creel to represent the
    collapsed 'all' estimate.

    """

    # stratum = models.ForeignKey(
    #    Strata, related_name="catch_estimates", on_delete=models.CASCADE
    # )

    fr712 = models.ForeignKey(
        FR712, related_name="catch_estimates", on_delete=models.CASCADE
    )

    species = models.ForeignKey(
        Species, related_name="catch_estimates", on_delete=models.CASCADE
    )

    #    creel = models.ForeignKey(FN011, related_name='catch_estimates')
    #
    #    season = models.ForeignKey(FN022, related_name='catch_estimates',
    #                              blank=True, null=True)
    #    dtp = models.ForeignKey(FN023, related_name='catch_estimates',
    #                            blank=True, null=True)
    #    period = models.ForeignKey(FN024, related_name='catch_estimates',
    #                               blank=True, null=True)
    #    area = models.ForeignKey(FN026, related_name='catch_estimates',
    #                             blank=True, null=True)
    #    mode = models.ForeignKey(FN028, related_name='catch_estimates',
    #                             blank=True, null=True)

    # NEW
    # run should be a fk to FR111 table
    # run = models.CharField(max_length=2, db_index=True)
    # rec_tp = models.IntegerField(default=2, choices=REC_TP_CHOICES)
    # strat = models.CharField(max_length=11)
    date = models.DateField(blank=False, null=True)
    sek = models.BooleanField()
    cif1_nn = models.IntegerField()

    angler1_s = models.IntegerField()
    rod1_s = models.IntegerField()
    mescnt_s = models.IntegerField(blank=True, null=True)
    meswt_s = models.FloatField(blank=True, null=True)

    catne1 = models.FloatField()
    catne1_pc = models.FloatField(blank=True, null=True)
    catne1_se = models.FloatField()
    catne1_vr = models.FloatField(blank=True, null=True)

    catne = models.FloatField()
    catne_se = models.FloatField()
    catne_vr = models.FloatField(blank=True, null=True)

    catno1_s = models.IntegerField()
    catno1_ss = models.IntegerField(blank=True, null=True)
    catno_s = models.IntegerField()
    catno_ss = models.IntegerField(blank=True, null=True)

    effae1 = models.FloatField()
    effae1_pc = models.FloatField(blank=True, null=True)
    effae1_se = models.FloatField()
    effae1_vr = models.FloatField(blank=True, null=True)

    effao1_s = models.FloatField()
    effao1_ss = models.FloatField(blank=True, null=True)

    effpe1 = models.FloatField()
    effpe1_se = models.FloatField(blank=True, null=True)
    effpe1_vr = models.FloatField(blank=True, null=True)

    effpo1_s = models.FloatField(blank=True, null=True)
    effpo1_ss = models.FloatField(blank=True, null=True)

    effre1 = models.FloatField()
    effre1_se = models.FloatField()
    effre1_vr = models.FloatField(blank=True, null=True)

    effro1_s = models.FloatField()
    effro1_ss = models.FloatField(blank=True, null=True)

    hvscat_pc = models.FloatField()

    hvsne = models.FloatField()
    hvsne_se = models.FloatField()
    hvsne_vr = models.FloatField(blank=True, null=True)

    hvsne1 = models.FloatField()
    hvsne1_se = models.FloatField()
    hvsne1_vr = models.FloatField(blank=True, null=True)

    cuenao = models.FloatField()
    cuenao1 = models.FloatField(blank=True, null=True)
    cuenae = models.FloatField()
    cuenae1 = models.FloatField(blank=True, null=True)

    hvsno_s = models.IntegerField()
    hvsno_ss = models.IntegerField(blank=True, null=True)

    hvsno1_s = models.IntegerField()
    hvsno1_ss = models.IntegerField(blank=True, null=True)

    catea_xy = models.FloatField(blank=True, null=True)
    catea1_xy = models.FloatField(blank=True, null=True)
    hvsea_xy = models.FloatField(blank=True, null=True)
    hvsea1_xy = models.FloatField(blank=True, null=True)
    cater_xy = models.FloatField(blank=True, null=True)
    cater1_xy = models.FloatField(blank=True, null=True)
    hvser_xy = models.FloatField(blank=True, null=True)
    hvser1_xy = models.FloatField(blank=True, null=True)
    catep_xy = models.FloatField(blank=True, null=True)
    catep1_xy = models.FloatField(blank=True, null=True)
    hvsep_xy = models.FloatField(blank=True, null=True)
    hvsep1_xy = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "HarvestEstimate"
        ##ordering = [
        #    "stratum__creel_run__creel__prj_cd",
        #    "stratum__creel_run__run",
        #    "stratum__stratum_label",
        #    "species",
        #    "date",
        #    "rec_tp",
        #    "sek",
        # ]
        unique_together = ["fr712", "species", "date", "sek"]

    def __str__(self):
        """return the object type (HarvestEstimate), and the prj_cd."""

        if self.date:
            repr = (
                "<HarvestEstimate: {}-{} sek:{} (prj_cd:{} run:{} rec_tp:{} date:{})>"
            )
            repr = repr.format(
                self.fr712.stratum.stratum_label,
                self.species.spc,
                self.sek,
                self.fr712.stratum.creel_run.creel.prj_cd,
                self.fr712.stratum.creel_run.run,
                self.fr712.rec_tp,
                self.date.strftime("%b-%d-%y"),
            )
        else:
            repr = "<HarvestEstimate: {}-{} sek:{} (prj_cd:{} run:{} rec_tp:{})>"
            repr = repr.format(
                self.fr712.stratum.stratum_label,
                self.species.spc,
                self.sek,
                self.fr712.stratum.creel_run.creel.prj_cd,
                self.fr712.stratum.creel_run.run,
                self.fr712.rec_tp,
            )

        return repr


class FR715(models.Model):
    """Class to hold angler options."""

    fr712 = models.ForeignKey(
        FR712, related_name="angler_options", on_delete=models.CASCADE
    )

    ang_fn = models.CharField(max_length=8, choices=ANG_FN_CHOICES)
    ang_val = models.CharField(max_length=4, blank=True, null=True)
    ang_freq = models.IntegerField()
    ang_prop = models.FloatField()
    pty_freq = models.IntegerField()
    pty_prop = models.FloatField()

    class Meta:
        app_label = "creel_portal"
        verbose_name = "Angler Options"

    def __str__(self):
        """return the object type (AnglerOption), and the prj_cd."""

        repr = "<AnglerOption: {}={} ({} run:{} strat:{} rec_tp:{})>"
        repr = repr.format(
            self.ang_fn,
            self.ang_val,
            self.fr712.stratum.creel_run.creel.prj_cd,
            self.fr712.stratum.creel_run.run,
            self.fr712.stratum.stratum_label,
            self.fr712.rec_tp,
        )

        return repr
