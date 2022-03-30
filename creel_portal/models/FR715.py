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

from .choices import ANG_FN_CHOICES


class FR715(models.Model):
    """Class to hold angler options."""

    fr712 = models.ForeignKey(
        "FR712", related_name="angler_options", on_delete=models.CASCADE
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
