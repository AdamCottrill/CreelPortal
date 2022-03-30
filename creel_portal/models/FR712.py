"""
=============================================================
~/creel_portal/creel_portal/models/FishNetResults.py
 Created: 30 Mar 2020 08:39:05

 DESCRIPTION:

 This file contains all of the results tables from a fishnet-II project:

 + FR712

 A. Cottrill
=============================================================
"""


from django.db import models

from .choices import REC_TP_CHOICES


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
        "Strata", on_delete=models.CASCADE, related_name="strata_attributes"
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
