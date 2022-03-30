"""
=============================================================
~/creel_portal/creel_portal/models/FR714.py
 Created: 30 Mar 2022 10:45:29

 DESCRIPTION:

 This file contains all of the results tables from a fishnet-II project:
 + FR714

 A. Cottrill
=============================================================
"""


from django.db import models

from common.models import Species


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
        "FR712", related_name="catch_estimates", on_delete=models.CASCADE
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
