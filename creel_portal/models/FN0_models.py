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
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from common.models import Lake

from .choices import CONTMETH_CHOICES

User = get_user_model()

# note = move this to main.models too
class FN011(models.Model):
    """Class to hold a record for each project"""

    lake = models.ForeignKey(
        Lake, default=1, related_name="creels", on_delete=models.CASCADE
    )

    prj_ldr = models.ForeignKey(
        User,
        help_text="Project Lead",
        related_name="creels",
        blank=False,
        on_delete=models.CASCADE,
    )
    field_crew = models.ManyToManyField(User, related_name="creel_crew")

    prj_date0 = models.DateField(help_text="Start Date", blank=False)
    prj_date1 = models.DateField(help_text="End Date", blank=False)
    prj_cd = models.CharField(
        help_text="Project Code", max_length=12, unique=True, blank=False
    )
    year = models.CharField(
        help_text="Year", max_length=4, blank=True, editable=False, db_index=True
    )
    prj_nm = models.CharField(help_text="Project Name", max_length=60, blank=False)

    comment0 = models.TextField(
        blank=True, null=True, help_text="General Project Description."
    )
    slug = models.SlugField(blank=True, unique=True, editable=False)

    # contmeth is repeated in FR711 table - will have to figure out how
    # to keep them in sync.
    contmeth = models.CharField(
        help_text="Creel Type",
        max_length=2,
        db_index=True,
        choices=CONTMETH_CHOICES,
        default="A2",
    )

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN011 - Creel"
        ordering = ["-prj_date1"]

    def get_absolute_url(self):
        """return the url for the project"""
        url = reverse("creel_portal:creel_detail", kwargs={"slug": self.slug})
        return url
        # return reverse("creel_detail", {"slug": self.slug})

    def __str__(self):
        """return the creel name and project code as its string
        representation"""
        return "<Creel: {} ({})>".format(self.prj_nm, self.prj_cd)

    def save(self, *args, **kwargs):
        """
        from:http://stackoverflow.com/questions/7971689/
             generate-slug-field-in-existing-table
        Slugify name if it doesn't exist. IMPORTANT: doesn't check to see
        if slug is a dupicate!
        """

        self.slug = slugify(self.prj_cd)
        self.year = self.prj_date0.year
        super(FN011, self).save(*args, **kwargs)

    def get_global_strata(self):
        """This function will return the global strata of the the last run of
        this creel. If the mask is "++_++_++_++", a single object will
        be returned correspondng to a single record in the FR712
        table. if the mask contains any ? - one record will be
        returned for each level in the corresponding stratum.
        """

        my_run = self.creel_run.order_by("-run").first()

        mask_re = my_run.strat_comb.replace("?", "\w").replace("+", "\+")

        my_strata = my_run.strata.filter(stratum_label__regex=mask_re).all()

        return my_strata

    def get_global_effort(self):
        """Return the final effort estimates for this creel at the highest
        level of aggregation.  If strat_comb indicates that all strata
        are to be collapsed, then the result is one element list
        containing the estimates.  If strat_comb indicates that one or
        more strata are not to be combined, this function returns a
        list with one element corresponding to each strata level.

        By default, the last run a creel is always returned.  This
        assumes that each run is an improvement on previous runs.
        This could be re-considered if necessary."""

        # get the globals for a creel:
        # return the estimates from the last run
        # TODO - we need to get multiple objects if the comb_strat contains
        # any '??'
        # effort = self.creel_run.order_by('-run').first().\
        #         strata.filter(stratum_label='++_++_++_++').\
        #         first().effort_estimates.get()

        my_run = self.creel_run.order_by("-run").first()

        mask_re = my_run.strat_comb.replace("?", "\w").replace("+", "\+")

        my_strata = my_run.strata.filter(stratum_label__regex=mask_re).all()

        estimates = []
        for x in my_strata:
            # strata = [x.season, x.daytype, x.period, x.area, x.mode]
            strata = x.stratum_label
            # tmp = x.effort_estimates.get()
            estimates.append({"strata": strata, "estimates": tmp})

        return estimates

    @property
    def final_run(self):
        """Return the final creel run - assumes that the run with the highest
        number is preferred. This may not be case.

        Arguments:
        - `self`:

        """
        return self.creel_run.order_by("-run").first()

    # def get_global_catch(self):
    #     """Return the final catch estimates for this creel at the highest
    #     level of aggregation.  If strat_comb indicates that all strata
    #     are to be collapsed, then the result is one element list
    #     containing the estimates.  If strat_comb indicates that one or
    #     more strata are not to be combined, this function returns a
    #     list with one element corresponding to each strata level.

    #     By default, the last run a creel is always returned.  This
    #     assumes that each run is an improvement on previous runs.
    #     This could be re-considered if necessary.

    #     """

    #     # catch_est = self.creel_run.order_by('-run').first().\
    #     #            strata.filter(stratum_label='++_++_++_++').\
    #     #            first().catch_estimates.all()
    #     # return catch_est

    #     my_run = self.creel_run.order_by("-run").first()

    #     mask_re = my_run.strat_comb.replace("?", "\w").replace("+", "\+")
    #     # my_strata = my_run.strata.filter(stratum_label__regex=mask_re).all()
    #     # estimates = []
    #     # for x in my_strata:
    #     #     # strata = [x.season, x.daytype, x.period, x.area, x.mode]
    #     #     strata = x.stratum_label
    #     #     #tmp = FR714.objects.filter(fr712__stratum=x)
    #     #     tmp = x.catch_estimates.all()
    #     #     estimates.append({"strata": strata, "estimates": tmp})

    #     return my_run.strata.filter(stratum_label__regex=mask_re).all()

    # def get_catch_totals(self):
    #     """this function returns a json string containing the observed and
    #     estimated catch and harvest numbers for this creel.

    #     If the creel has only one final strata, this query should
    #     return numbers that are exactly the same as the global strata
    #     (++_++_++_++), but in cases where strata are maintained
    #     seperatately (and that strata does not exist), this query
    #     returns the equivalent values by summing accross all
    #     individual strata estiamtes.

    #     TODO: this function should be exposed through an api.

    #     Arguments:
    #     - `self`:

    #     """
    #     # aliases = {"common_name": F("species__common_name")}

    #     # aggregation_metrics = {
    #     #     "xcatne": Sum("catne"),
    #     #     "xcatne1": Sum("catne1"),
    #     #     "xcatno_s": Sum("catno_s"),
    #     #     "xcatno1_s": Sum("catno1_s"),
    #     #     "xhvsno_s": Sum("hvsno_s"),
    #     #     "xhvsno1_s": Sum("hvsno1_s"),
    #     #     "xhvsne": Sum("hvsne"),
    #     #     "xhvsne1": Sum("hvsne1"),
    #     # }

    #     # catch_counts = (
    #     #     FR714.objects.filter(stratum__creel_run=self.final_run, rec_tp=2)
    #     #     .annotate(**aliases)
    #     #     .values("common_name")
    #     #     .order_by()
    #     #     .annotate(**aggregation_metrics)
    #     # )

    #     # return json.dumps(list(catch_counts))

    #     return None


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


class FN023(models.Model):
    """Class  to represent the daytypes used in each season of creel"""

    DAYTYPE_CHOICES = ((1, "weekday"), (2, "weekend"))

    # creel = models.ForeignKey(FN011)
    season = models.ForeignKey(FN022, related_name="daytypes", on_delete=models.CASCADE)
    dtp = models.CharField(
        help_text="Day Type Code",
        max_length=2,
        blank=False,
        db_index=True,
        choices=DAYTYPE_CHOICES,
    )
    dtp_nm = models.CharField(help_text="Day Type Name", max_length=10, blank=False)
    dow_lst = models.CharField(help_text="Day Of Week List", max_length=7, blank=False)

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN023 - Day Type"
        ordering = ["dtp"]
        unique_together = ["season", "dtp"]

    @property
    def creel(self):
        """A shortcut method to directly access the creel object - allows use
        of same permission class on different api endpoints.
        """
        return self.season.creel

    def save(self, *args, **kwargs):
        """ """

        raw_slug = "-".join([self.season.creel.prj_cd, self.season.ssn, self.dtp])

        self.slug = slugify(raw_slug)
        super(FN023, self).save(*args, **kwargs)

    def __str__(self):
        """return the object type, the daytype name, day type code, and the
        code project code of the creel this record is assoicated with.

        """

        repr = "<DayType: {}({}) {}-{}>"
        return repr.format(
            self.dtp_nm, self.dtp, self.season.ssn, self.season.creel.prj_cd
        )

    @property
    def label(self):
        """a string that will be used in serialized respoonse for this strata.
        If both the dtp, and dtp des are available, return them, otherwise,
        return just the snn code.

        Arguments:
        - `self`:

        """
        if self.dtp_nm:
            label = "{}-{}".format(self.dtp, self.dtp_nm.title())
        else:
            label = "{}".format(self.dtp)
        return label


class FN024(models.Model):
    """Class to represent the period used in each day types of each season
    of creel.
    """

    daytype = models.ForeignKey(FN023, related_name="periods", on_delete=models.CASCADE)
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


class FN025(models.Model):
    """Class to represent the day type exceptions so that holidays can be
    treated as weekends.
    """

    season = models.ForeignKey(
        FN022, related_name="exception_dates", on_delete=models.CASCADE
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
                {"date": _("Date occurs before the associated season.")}
            )

        if self.date > self.season.ssn_date1.date():
            raise ValidationError(
                {"date": _("Date occurs after the associated season.")}
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


class FN026(models.Model):
    """Class to represent the spatial strat used in a creel."""

    creel = models.ForeignKey(
        "FN011", related_name="spatial_strata", on_delete=models.CASCADE
    )
    space = models.CharField(
        max_length=2, blank=False, help_text="Space Code", db_index=True
    )
    space_des = models.CharField(
        max_length=100, blank=False, help_text="Space Description"
    )
    space_siz = models.IntegerField(blank=True, null=True)
    area_cnt = models.IntegerField(blank=True, null=True)
    area_lst = models.CharField(
        max_length=20, help_text="Area List", blank=True, null=True
    )
    area_wt = models.FloatField(blank=True, null=True)

    label = models.CharField(max_length=110, blank=False, help_text="Space Label")

    slug = models.SlugField(blank=True, unique=True, editable=False)

    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN026 - Spatial Strata"
        verbose_name_plural = "FN026 - Spatial Strata"
        ordering = ["space"]
        unique_together = ["creel", "space"]

    def __str__(self):
        """return the object type, the space name, the space code, and
        project code of the creel this record is assoicated with.

        """

        repr = "<Space: {} ({}) [{}]>"
        return repr.format(self.space_des, self.space, self.creel.prj_cd)

    def save(self, *args, **kwargs):
        """
        Create a space label as a combination of the space description
        and space code.
        """

        raw_slug = "-".join([self.creel.prj_cd, self.space])

        self.slug = slugify(raw_slug)

        if self.space_des:
            self.label = "{}-{}".format(self.space, self.space_des.title())
        else:
            self.label = "{}".format(self.space)
        super(FN026, self).save(*args, **kwargs)


#    @property
#    def label(self):
#        """a string that will be used in serialized respoonse for this strata.
#        If both the space, and space_des are available, return them, otherwise,
#        return just the snn code.
#
#        Arguments:
#        - `self`:
#
#        """
#        if self.space_des:
#            label = '{}-{}'.format(self.space, self.space_des.title())
#        else:
#            label = '{}'.format(self.space)
#        return label
#
#
#    @property
#    def popupContent(self):
#        if self.space_des:
#            return "<p>Space: {} ({})</p>".format(self.space_des.title(),
#                                                  self.space)
#        else:
#            return "<p>Space: {}</p>".format(self.space)
#


class FN028(models.Model):
    """Class to represent the fishing modes used in a creel."""

    UNIT_CHOICES = ((1, "person"), (2, "party"))

    CHKFLAG_CHOICES = ((0, "No"), (1, "Yes"))

    creel = models.ForeignKey("FN011", related_name="modes", on_delete=models.CASCADE)
    mode = models.CharField(
        help_text="Mode Code", max_length=2, blank=False, db_index=True
    )
    mode_des = models.CharField(
        help_text="Fishing Mode Description", max_length=100, blank=False
    )
    atyunit = models.IntegerField(
        help_text="Activity Unit", default=1, choices=UNIT_CHOICES
    )
    itvunit = models.IntegerField(
        help_text="Interview Unit", default=1, choices=UNIT_CHOICES
    )
    chkflag = models.IntegerField(
        help_text="Check Flag", default=0, choices=CHKFLAG_CHOICES
    )

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN028 - Fishing Mode"
        ordering = ["mode"]
        unique_together = ["creel", "mode"]

    def __str__(self):
        """return the object type, the mode name, the mode code, and
        project code of the creel this record is assoicated with.

        """

        repr = "<FishingMode: {} ({}) [{}]>"
        return repr.format(self.mode_des, self.mode, self.creel.prj_cd)

    @property
    def label(self):
        """a string that will be used in serialized respoonse for this strata.
        If both the mode, and mode_des are available, return them, otherwise,
        return just the snn code.

        Arguments:
        - `self`:

        """
        if self.mode_des:
            label = "{}-{}".format(self.mode, self.mode_des.title())
        else:
            label = "{}".format(self.mode)
        return label

    def save(self, *args, **kwargs):
        """Create a unique slug for each fishing mode in this creel."""

        raw_slug = "-".join([self.creel.prj_cd, self.mode])
        self.slug = slugify(raw_slug)
        super(FN028, self).save(*args, **kwargs)


class FN111(models.Model):
    """Class to represent the creel logs."""

    # from FN-2 data dictionary
    WEATHER_CHOICES = [(0, "No effect"), (1, "Possible effect"), (2, "Definite effect")]

    # stratum = models.ForeignKey(Strata, related_name='interview_logs')
    creel = models.ForeignKey(
        "FN011", related_name="interview_logs", on_delete=models.CASCADE
    )
    season = models.ForeignKey(
        FN022, related_name="interview_logs", on_delete=models.CASCADE
    )
    daytype = models.ForeignKey(
        FN023, related_name="interview_logs", on_delete=models.CASCADE
    )
    period = models.ForeignKey(
        FN024, related_name="interview_logs", on_delete=models.CASCADE
    )
    area = models.ForeignKey(
        FN026, related_name="interview_logs", on_delete=models.CASCADE
    )
    mode = models.ForeignKey(
        FN028, related_name="interview_logs", on_delete=models.CASCADE
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


class FN112(models.Model):
    """Class to represent the activity counts associated with a creel log."""

    sama = models.ForeignKey(
        FN111, related_name="activity_counts", on_delete=models.CASCADE
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
