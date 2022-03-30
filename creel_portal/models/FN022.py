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

from datetime import datetime, timedelta

from django.db import models
from django.template.defaultfilters import slugify

from django.utils.translation import gettext_lazy as _


class FN022(models.Model):
    """Class to represent the seasons (temporal strata) used in each creel."""

    creel = models.ForeignKey("FN011", related_name="seasons", on_delete=models.CASCADE)
    ssn = models.CharField(
        help_text="Season Code", max_length=2, blank=False, db_index=True
    )
    ssn_des = models.CharField(
        help_text="Season Description", max_length=60, blank=False
    )
    ssn_date0 = models.DateField(help_text="Season Start Date", blank=False)
    ssn_date1 = models.DateField(help_text="Season End Date", blank=False)

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN022 - Season"
        ordering = ["ssn"]
        unique_together = ["creel", "ssn"]

    def save(self, *args, **kwargs):
        """ """

        raw_slug = "-".join([self.creel.prj_cd, self.ssn])

        self.slug = slugify(raw_slug)
        super(FN022, self).save(*args, **kwargs)

    def __str__(self):
        """return the season name, code and project code associated with this
        particular season."""

        repr = "<Season: {} ({}) [{}]>"
        return repr.format(self.ssn_des, self.ssn, self.creel.prj_cd)

    @property
    def label(self):
        """a string that will be used in serialized respoonse for this strata.
        If both the ssn, and ssn des are available, return them, otherwise,
        return just the snn code.

        Arguments:
        - `self`:

        """
        if self.ssn_des:
            label = "{}-{}".format(self.ssn, self.ssn_des.title())
        else:
            label = "{}".format(self.ssn)
        return label

    def tally_days(self):
        """a helper function that returns a three element dictionary contains
        the the total number of days covered by this season, the
        number of weekdays, and the number of weekend days.  Exception
        dates and holidays are not included here - they are applied
        when the actualy stratum values are calculated.

        """

        ssn_start = self.ssn_date0
        ssn_end = self.ssn_date1

        # the total number of days in the season including the last day
        total_days = (ssn_end - ssn_start).days + 1
        daygenerator = (ssn_start + timedelta(x) for x in range(total_days))

        # weekdays:
        weekdays = sum(day.weekday() < 5 for day in daygenerator)
        # weekends are the difference
        weekend_days = total_days - weekdays

        return dict(total_days=total_days, weekend_days=weekend_days, weekdays=weekdays)

    def get_strat_days(self, dtp="1"):
        """Given a daytype code, return the corresponding number of days in
        this strata.  There is no guarantee that all creel will use
        dtp=2 for weekends (dow_lst=17).  This will return them either
        way, as long as 17 was used for saturday-sunday.
        """

        dow_list = self.daytypes.get(dtp=dtp).dow_lst
        if dow_list == "17":
            days = self.tally_days().get("weekend_days")
        else:
            days = self.tally_days().get("weekdays")

        exception_dates = self.exception_dates.all()
        for x in exception_dates:
            if x.dtp1 == dtp:
                days += 1
            else:
                days -= 1

        return days
