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


class FN024(models.Model):
    """Class to represent the period used in each day types of each season
    of creel.
    """

    daytype = models.ForeignKey(
        "FN023", related_name="periods", on_delete=models.CASCADE
    )
    prd = models.CharField(
        help_text="Period Code", max_length=2, blank=False, db_index=True
    )
    prdtm0 = models.TimeField(help_text="Period Start Time", blank=False)
    prdtm1 = models.TimeField(help_text="Period End Time", blank=False)
    prd_dur = models.FloatField(help_text="Period Duration (hrs)", blank=False)

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN024 - Period"
        ordering = ["prd"]
        unique_together = ["daytype", "prd"]

    def __str__(self):
        """return the object type, period code, the daytype name, the season,
        and project code of the creel this record is assoicated with.

        """

        start = self.prdtm0.strftime("%H:%M")
        end = self.prdtm1.strftime("%H:%M")

        repr = "<Period: {} ({}-{} ({} hrs)) {}-{}-{}>"
        return repr.format(
            self.prd,
            start,
            end,
            self.prd_dur,
            self.daytype.dtp_nm,
            self.daytype.season.ssn_des,
            self.daytype.season.creel.prj_cd,
        )

    def save(self, *args, **kwargs):
        """
        Create a space label as a combination of the space description
        and space code.
        """

        raw_slug = "-".join(
            [
                self.daytype.season.creel.prj_cd,
                self.daytype.season.ssn,
                self.daytype.dtp,
                str(self.prd),
            ]
        )

        self.slug = slugify(raw_slug)

        # to calculate the difference between times, we need to convert
        # them to date.  Use the current date, it won't affect the results
        adate = datetime.now().date()
        delta = datetime.combine(adate, self.prdtm1) - datetime.combine(
            adate, self.prdtm0
        )

        self.prd_dur = delta.total_seconds() / (60 * 60)
        super(FN024, self).save(*args, **kwargs)

    @property
    def creel(self):
        """A shortcut method to directly access the creel object - allows use
        of same permission class on different api endpoints.
        """
        return self.daytype.season.creel
