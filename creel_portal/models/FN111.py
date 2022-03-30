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
from django.urls import reverse

from .FN022 import FN022
from .FN023 import FN023
from .FN024 import FN024
from .FN025 import FN025
from .FN026 import FN026


class FN111(models.Model):
    """Class to represent the creel logs."""

    # from FN-2 data dictionary
    WEATHER_CHOICES = [(0, "No effect"), (1, "Possible effect"), (2, "Definite effect")]

    # stratum = models.ForeignKey(Strata, related_name='interview_logs')
    creel = models.ForeignKey(
        "FN011", related_name="interview_logs", on_delete=models.CASCADE
    )
    season = models.ForeignKey(
        "FN022", related_name="interview_logs", on_delete=models.CASCADE
    )
    daytype = models.ForeignKey(
        "FN023", related_name="interview_logs", on_delete=models.CASCADE
    )
    period = models.ForeignKey(
        "FN024", related_name="interview_logs", on_delete=models.CASCADE
    )
    area = models.ForeignKey(
        "FN026", related_name="interview_logs", on_delete=models.CASCADE
    )
    mode = models.ForeignKey(
        "FN028", related_name="interview_logs", on_delete=models.CASCADE
    )

    sama = models.CharField(max_length=6, blank=False)
    date = models.DateField(blank=False, db_index=True)
    samtm0 = models.TimeField(blank=False, help_text="Interview Period Start")
    weather = models.IntegerField(choices=WEATHER_CHOICES, blank=True, null=True)

    help_str = "Comments about current interview period."
    comment1 = models.TextField(
        max_length=200, blank=True, null=True, help_text=help_str
    )
    daycode = models.CharField(max_length=1, blank=False, db_index=True)

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN111 - Inveriew Log"
        ordering = ["creel__prj_cd", "sama"]
        unique_together = ["creel", "sama"]

    def __str__(self):
        """return the object type, the interview log number (sama), the stratum,
         and project code of the creel this record is assoicated
        with.

        """

        repr = "<InterviewLog: {} ({})>"
        return repr.format(self.sama, self.creel.prj_cd)

    def save(self, *args, **kwargs):
        """Create a unique slug for each fishing mode in this creel."""

        raw_slug = "-".join([self.creel.prj_cd, self.sama])
        self.slug = slugify(raw_slug)
        super(FN111, self).save(*args, **kwargs)

    @property
    def dow(self):
        """Return the numeric day of the week of the interview log.
        Sunday=1, Saturday=7.

        Arguments:
        - `self`:
        """
        dow = int(datetime.strftime(self.date, "%w")) + 1
        return dow

    def check_exception_date(self):
        """Returns true if the date of this samlog occurs on a known exception date."""
        exception = (
            FN025.objects.filter(season=self.season).filter(date=self.date).first()
        )

        return True if exception else False

    def check_daytype(self):
        """get the day type associated with this interview log.  The day type
        is determined by the creel, season, and date.  If a record
        exsits for this date in the exception dates table (FN025) use it,
        otherwise get the day type from the FN024 table.

        Arguments:
        - `self`:

        """
        daytype = (
            FN023.objects.filter(season=self.season)
            .filter(dow_lst__contains=self.dow)
            .first()
        )

        return self.daytype == daytype

    def check_period(self):
        """get the period associated with this interview log.  The period is
        determined by the creel, season, date, and start time.

        Arguments:
        - `self`:

        """
        period = (
            FN024.objects.filter(daytype=self.daytype)
            .filter(prdtm0__lte=self.samtm0)
            .order_by("-prdtm0")
            .first()
        )
        # return period
        return self.period == period

    def check_season(self):
        """Given the project_code and date, return the corresponding season
        for this creel log by finding the season that has start and
        end dates span the date of the creel log.

        Arguments:
        - `self`:

        """

        mydate = self.date
        ssn = (
            FN022.objects.filter(creel=self.creel)
            .filter(ssn_date0__lte=mydate)
            .filter(ssn_date1__gte=mydate)
            .get()
        )

        # True if  the season is correct, false otherwise
        return self.season == ssn

    @property
    def stratum(self):
        """the stratum method should return the space, mode, day type,
        period and season of an interview log, as a FishNet-2 stratum
        string of the form: "XX_XX_XX_XX (SSN_[DayType][Period]_Area_Mode)."

        """
        myseason = self.season.ssn
        myspace = self.area.space
        myperiod = self.period.prd
        mydaytype = self.daytype.dtp
        mymode = self.mode.mode

        repr = "{}_{}{}_{}_{}".format(myseason, mydaytype, myperiod, myspace, mymode)
        return repr

        return self.stratum.stratum
