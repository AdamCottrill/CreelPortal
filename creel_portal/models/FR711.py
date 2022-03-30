"""
=============================================================
~/creel_portal/creel_portal/models/FishNetResults.py
 Created: 30 Mar 2020 08:39:05

 DESCRIPTION:

 This file contains all of the results tables from a fishnet-II project:

 + FR711

 A. Cottrill
=============================================================
"""


from django.db import models

from .choices import CONTMETH_CHOICES, REC_TP_CHOICES, ANG_FN_CHOICES


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
