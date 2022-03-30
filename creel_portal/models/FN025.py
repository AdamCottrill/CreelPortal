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
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy


class FN025(models.Model):
    """Class to represent the day type exceptions so that holidays can be
    treated as weekends.
    """

    season = models.ForeignKey(
        "FN022", related_name="exception_dates", on_delete=models.CASCADE
    )
    date = models.DateField(help_text="Exception Date", blank=False)
    dtp1 = models.CharField(help_text="Day Type Code", max_length=2, blank=False)
    description = models.CharField(
        help_text="Description", max_length=50, default="Holiday"
    )

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN025 - Exception Date"
        ordering = ["date"]
        unique_together = ["season", "date"]

    def clean(self):
        """The exception date must fall within the dates of the assoicated season."""

        if self.date < self.season.ssn_date0.date():
            raise ValidationError(
                {"date": gettext_lazy("Date occurs before the associated season.")}
            )

        if self.date > self.season.ssn_date1.date():
            raise ValidationError(
                {"date": gettext_lazy("Date occurs after the associated season.")}
            )

    def save(self, *args, **kwargs):
        """
        Create a slug as a combination of the prject code, the season code and the date.

        """

        raw_slug = "-".join(
            [self.season.creel.prj_cd, self.season.ssn, self.date.strftime("%Y-%m-%d")]
        )

        self.slug = slugify(raw_slug)
        self.full_clean()
        super(FN025, self).save(*args, **kwargs)

    def __str__(self):
        """return the object type, the date, the season name, and
        code project code of the creel this record is assoicated with.

        """
        fdate = datetime.strftime(self.date, "%Y-%m-%d")
        repr = "<ExceptionDate: {} ({}-{})>"
        return repr.format(fdate, self.season.ssn_des, self.season.creel.prj_cd)

    @property
    def creel(self):
        """A shortcut method to directly access the creel object - allows use
        of same permission class on different api endpoints.
        """
        return self.season.creel
