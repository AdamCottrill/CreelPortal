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


class FR713(models.Model):
    """Class to hold creel estimate of effort by strata.

    TODO - figure out if we need strat, if it should be build
    dynamically or ahead of time or if a '++' placeholder should be
    created add to each stratum of each creel to represent the
    collapsed 'all' estimate.

    """

    fr712 = models.ForeignKey(
        "FR712", related_name="effort_estimates", on_delete=models.CASCADE
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
