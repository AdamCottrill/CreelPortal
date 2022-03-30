"""=============================================================
~/creel_portal/creel_portal/models/CreelTables.py
 Created: 30 Mar 2020 08:49:17

 DESCRIPTION:

  This file contains all of the design tables from a
  fishnet-II/Creesys project that are specific to creels.

+ FN022
+ FN023
+ FN024
+ FN025
+ FN026
+ FN028
+ FN111
+ FN112
+ Strata


 A. Cottrill
=============================================================

"""

from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify


class FN112(models.Model):
    """Class to represent the activity counts associated with a creel log."""

    sama = models.ForeignKey(
        "FN111", related_name="activity_counts", on_delete=models.CASCADE
    )

    atytm0 = models.TimeField(blank=False, help_text="Period Start")
    atytm1 = models.TimeField(blank=False, help_text="Period End")
    atycnt = models.IntegerField(default=0, help_text="Activity Count")
    chkcnt = models.IntegerField(
        blank=True, null=True, default=0, help_text="Check Count"
    )
    itvcnt = models.IntegerField(default=0, help_text="Interview Count")

    atydur = models.FloatField(help_text="Period Duration", default=0)

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN112 - Activity Count"
        ordering = ["sama", "atytm0", "atytm1"]
        unique_together = ["sama", "atytm0", "atytm1"]

    def __str__(self):
        """return the object type, project code, the interview log
        number (sama), the start time, and the end time.
        """

        repr = "ActivityCount: {}-{} {}-{}"
        return repr.format(
            self.sama.creel.prj_cd, self.sama.sama, self.atytm0, self.atytm1
        )

    def save(self, *args, **kwargs):
        """ """

        # to calculate the difference between times, we need to convert
        # them to date.  Use the current date, it won't affect the results
        anydate = datetime.now().date()
        delta = datetime.combine(anydate, self.atytm1) - datetime.combine(
            anydate, self.atytm0
        )
        self.atydur = delta.total_seconds() / (60 * 60)
        ts = self.atytm0.strftime("%H:%M")
        raw_slug = "-".join([self.sama.creel.prj_cd, self.sama.sama, ts])
        self.slug = slugify(raw_slug)

        super(FN112, self).save(*args, **kwargs)
