from django.db import models

# from django.core.serializers.json import DjangoJSONEncoder

# from django.core import serializers
from django.db.models import Sum, F
from django.template.defaultfilters import slugify
from django.urls import reverse

# from aldjemy.meta import AldjemyMeta
# from sqlalchemy import func

from datetime import datetime, timedelta

import json

# Create your models here.

# note = move this to main.models
class Species(models.Model):
    species_code = models.IntegerField(unique=True)
    common_name = models.CharField(max_length=30)
    scientific_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ["species_code"]

    def __str__(self):
        if self.scientific_name:
            spc_str = "<Species: %s (%s)>" % (self.common_name, self.scientific_name)
        else:
            spc_str = "<Species: %s>" % self.common_name
        return spc_str


# note = move this to main.models
class Lake(models.Model):
    """A lookup table to hold the names of the different lakes"""

    abbrev = models.CharField(max_length=10, unique=True)
    lake_name = models.CharField(max_length=50)

    ddlat = models.FloatField(default=45.0)
    ddlon = models.FloatField(default=-82.0)
    zoom = models.IntegerField(default=7)

    class Meta:
        verbose_name = "Lake"

    def __str__(self):
        """return the lake name as its string representation"""
        return "<Lake: {} ({})>".format(self.lake_name, self.abbrev)


# note = move this to main.models too
class FN011(models.Model):
    """Class to hold a record for each project
    """

    lake = models.ForeignKey(
        Lake, default=1, related_name="creels", on_delete=models.CASCADE
    )

    prj_date0 = models.DateField(help_text="Start Date", blank=False)
    prj_date1 = models.DateField(help_text="End Date", blank=False)
    prj_cd = models.CharField(
        help_text="Project Code", max_length=12, unique=True, blank=False
    )
    year = models.CharField(help_text="Year", max_length=4, blank=True, editable=False)
    prj_nm = models.CharField(help_text="Project Name", max_length=60, blank=False)
    prj_ldr = models.CharField(help_text="Project Lead", max_length=40, blank=False)
    comment0 = models.TextField(
        blank=True, null=True, help_text="General Project Description."
    )
    slug = models.SlugField(blank=True, unique=True, editable=False)

    aru = models.TextField(blank=True, null=True)
    fof_loc = models.TextField(blank=True, null=True)
    fof_nm = models.TextField(blank=True, null=True)
    wby = models.TextField(blank=True, null=True)
    wby_nm = models.TextField(blank=True, null=True)
    prj_his = models.TextField(blank=True, null=True)
    prj_size = models.TextField(blank=True, null=True)
    prj_ver = models.TextField(blank=True, null=True)
    v0 = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Creel List"
        ordering = ["-prj_date1"]

    def get_absolute_url(self):
        """return the url for the project"""
        url = reverse("creel_detail", kwargs={"slug": self.slug})
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
            tmp = x.effort_estimates.get()
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

    def get_global_catch(self):
        """Return the final catch estimates for this creel at the highest
        level of aggregation.  If strat_comb indicates that all strata
        are to be collapsed, then the result is one element list
        containing the estimates.  If strat_comb indicates that one or
        more strata are not to be combined, this function returns a
        list with one element corresponding to each strata level.

        By default, the last run a creel is always returned.  This
        assumes that each run is an improvement on previous runs.
        This could be re-considered if necessary.

        """

        # catch_est = self.creel_run.order_by('-run').first().\
        #            strata.filter(stratum_label='++_++_++_++').\
        #            first().catch_estimates.all()
        # return catch_est

        my_run = self.creel_run.order_by("-run").first()

        mask_re = my_run.strat_comb.replace("?", "\w").replace("+", "\+")
        my_strata = my_run.strata.filter(stratum_label__regex=mask_re).all()
        estimates = []
        for x in my_strata:
            # strata = [x.season, x.daytype, x.period, x.area, x.mode]
            strata = x.stratum_label
            tmp = x.catch_estimates.all()
            estimates.append({"strata": strata, "estimates": tmp})

        return estimates

    def get_catch_totals(self):
        """this function returns a json string containing the observed and
        estimated catch and harvest numbers for this creel.

        If the creel has only one final strata, this query should
        return numbers that are exactly the same as the global strata
        (++_++_++_++), but in cases where strata are maintained
        seperatately (and that strata does not exist), this query
        returns the equivalent values by summing accross all
        individual strata estiamtes.

        TODO: this function should be exposed through an api.

        Arguments:
        - `self`:

        """

        aliases = {"common_name": F("species__common_name")}

        aggregation_metrics = {
            "xcatne": Sum("catne"),
            "xcatne1": Sum("catne1"),
            "xcatno_s": Sum("catno_s"),
            "xcatno1_s": Sum("catno1_s"),
            "xhvsno_s": Sum("hvsno_s"),
            "xhvsno1_s": Sum("hvsno1_s"),
            "xhvsne": Sum("hvsne"),
            "xhvsne1": Sum("hvsne1"),
        }

        catch_counts = (
            FR714.objects.filter(stratum__creel_run=self.final_run, rec_tp=2)
            .annotate(**aliases)
            .values("common_name")
            .order_by()
            .annotate(**aggregation_metrics)
        )

        return json.dumps(list(catch_counts))


class FN022(models.Model):
    """Class to represent the seasons (temporal strata) used in each creel.
    """

    creel = models.ForeignKey(FN011, related_name="seasons", on_delete=models.CASCADE)
    ssn = models.CharField(help_text="Season Code", max_length=2, blank=False)
    ssn_des = models.CharField(
        help_text="Season Description", max_length=60, blank=False
    )
    ssn_date0 = models.DateField(help_text="Season Start Date", blank=False)
    ssn_date1 = models.DateField(help_text="Season End Date", blank=False)

    v0 = models.CharField(max_length=4, blank=False)

    class Meta:
        verbose_name = "Seasons"
        ordering = ["ssn"]
        unique_together = ["creel", "ssn"]

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
    """Class  to represent the daytypes used in each season of creel
    """

    # creel = models.ForeignKey(FN011)
    season = models.ForeignKey(FN022, related_name="daytypes", on_delete=models.CASCADE)
    dtp = models.CharField(help_text="Day Type Code", max_length=2, blank=False)
    dtp_nm = models.CharField(help_text="Day Type Name", max_length=10, blank=False)
    dow_lst = models.CharField(help_text="Day Of Week List", max_length=7, blank=False)

    class Meta:
        verbose_name = "Day Types"
        ordering = ["dtp"]
        unique_together = ["season", "dtp"]

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
    prd = models.CharField(help_text="Day Type Code", max_length=2, blank=False)
    prdtm0 = models.TimeField(help_text="Period Start Time", blank=False)
    prdtm1 = models.TimeField(help_text="Period End Time", blank=False)
    prd_dur = models.FloatField(help_text="Period Duration (hrs)", blank=False)

    class Meta:
        verbose_name = "Periods"
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
        """from:http://stackoverflow.com/questions/7971689/
             generate-slug-field-in-existing-table

        Create a space label as a combination of the space description
        and space code.
        """

        # to calculate the difference between times, we need to convert
        # them to date.  Use the current date, it won't affect the results
        adate = datetime.now().date()
        delta = datetime.combine(adate, self.prdtm1) - datetime.combine(
            adate, self.prdtm0
        )

        self.prd_dur = delta.total_seconds() / (60 * 60)
        super(FN024, self).save(*args, **kwargs)


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

    class Meta:
        verbose_name = "Exception Dates"
        ordering = ["date"]

    #    def get_dtp_nm(self):
    #        """the day types are stored in the FN023 table.  We want to return
    #        dpt_nm from FN023 where the season and dpt match."""
    #
    #        dtp_nm = FN023.objects.filter(season=self.season,
    #                                      dtp=self.dpt1).values('dpt_name')[0]
    #        return dpt_nm

    def __str__(self):
        """return the object type, the date, the season name, and
       code project code of the creel this record is assoicated with.

        """
        fdate = datetime.strftime(self.date, "%Y-%m-%d")
        repr = "<ExceptionDate: {} ({}-{})>"
        return repr.format(fdate, self.season.ssn_des, self.season.creel.prj_cd)


class FN026(models.Model):
    """Class to represent the spatial strat used in a creel.
    """

    creel = models.ForeignKey(
        FN011, related_name="spatial_strata", on_delete=models.CASCADE
    )
    space = models.CharField(max_length=2, blank=False, help_text="Space Code")
    space_des = models.CharField(
        max_length=100, blank=False, help_text="Space Description"
    )
    space_siz = models.IntegerField(blank=True, null=True)
    area_cnt = models.IntegerField(blank=True, null=True)
    area_lst = models.CharField(
        max_length=2, help_text="Area List", blank=True, null=True
    )
    area_wt = models.FloatField(blank=True, null=True)

    label = models.CharField(max_length=110, blank=False, help_text="Space Label")

    ddlat = models.FloatField(blank=True, null=True)
    ddlon = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Spatial Strata"
        ordering = ["space"]
        unique_together = ["creel", "space"]

    def __str__(self):
        """return the object type, the space name, the space code, and
       project code of the creel this record is assoicated with.

        """

        repr = "<Space: {} ({}) [{}]>"
        return repr.format(self.space_des, self.space, self.creel.prj_cd)

    def save(self, *args, **kwargs):
        """from:http://stackoverflow.com/questions/7971689/
             generate-slug-field-in-existing-table

        Create a space label as a combination of the space description
        and space code.
        """

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
    """Class to represent the fishing modes used in a creel.
    """

    CHKFLAG_CHOICES = ((0, "No"), (1, "Yes"))

    creel = models.ForeignKey(FN011, related_name="modes", on_delete=models.CASCADE)
    mode = models.CharField(help_text="Mode Code", max_length=2, blank=False)
    mode_des = models.CharField(
        help_text="Fishing Mode Description", max_length=100, blank=False
    )
    atyunit = models.IntegerField(help_text="Activity Unit")
    itvunit = models.IntegerField(help_text="Interview Unit")
    chkflag = models.IntegerField(
        help_text="Check Flag", default=0, choices=CHKFLAG_CHOICES
    )

    class Meta:
        verbose_name = "Fishing Mode"
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


class FR711(models.Model):
    """Class to hold creel strata settings.  this table contains
    information about contact method (access or roving creel), whether or
    not estimates are save daily, and which strata can be combined or must
    be estimated separately (important for presenting final results as
    there may not be a ++_++_++_++ strata.

    """

    CONTMETH_CHOICES = (
        ("A2", "Access; Same days"),
        ("R0", "Roving; No interviews"),
        ("R1", "Roving; Not same days"),
        ("R2", "Roving; Same days"),
    )

    FR71_UNIT_CHOICES = ((0, "Rods"), (1, "Anglers"), (2, "Parties"))

    FR71_EST_CHOICES = ((1, "1-stage"), (2, "2-stage"))

    creel = models.ForeignKey(FN011, related_name="creel_run", on_delete=models.CASCADE)
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
        verbose_name = "EffortEstimate"
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


class Strata(models.Model):
    """A table that lies at the intersection of the design and data
    tables.  For new creels, we may want to add a build method that will
    create the stratum table using the cartesian product of all strata in
    the creel plus any defined in FR711
    """

    creel_run = models.ForeignKey(
        FR711, related_name="strata", on_delete=models.CASCADE
    )

    stratum_label = models.CharField(max_length=11)

    # optional foreign keys:
    season = models.ForeignKey(
        FN022, related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    daytype = models.ForeignKey(
        FN023, related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    period = models.ForeignKey(
        FN024, related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    area = models.ForeignKey(
        FN026, related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    mode = models.ForeignKey(
        FN028, related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["creel_run", "stratum_label"]
        ordering = ["creel_run__creel__prj_cd", "creel_run__run", "stratum_label"]

    def __str__(self):
        """return the object type, the interview log number (sama), the stratum,
        and project code of the creel this record is assoicated
       with.

        """

        repr = "{}(run:{}): {}"
        return repr.format(
            self.creel_run.creel.prj_cd, self.creel_run.run, self.stratum_label
        )

    @property
    def strat_days(self):
        """Not sure if this should be a property or a field that this updated
        on save().

        Arguments:
        - `self`:
        """
        return self.calc_strat_days()

    @property
    def strat_hours(self):
        """Not sure if this should be a property or a field that this updated
        on save().

        Arguments:
        - `self`:

        """
        return self.calc_strat_hours()

    def calc_strat_days(self):
        """"""
        dtp = self.daytype.dtp
        days = self.season.get_strat_days(dtp)
        return days

    def calc_strat_hours(self):
        """"""
        days = self.calc_strat_days()
        prd_dir = self.period.prd_dur
        return days * prd_dir


class FN111(models.Model):
    """Class to represent the creel logs.
    """

    # stratum = models.ForeignKey(Strata, related_name='interview_logs')
    creel = models.ForeignKey(
        FN011, related_name="interview_logs", on_delete=models.CASCADE
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
    weather = models.CharField(max_length=200, blank=False)
    help_str = "Comments about current interview period."
    comment1 = models.CharField(
        max_length=200, blank=True, null=True, help_text=help_str
    )
    daycode = models.CharField(max_length=1, blank=False, db_index=True)

    class Meta:
        verbose_name = "Inveriew Log"
        ordering = ["creel__prj_cd", "sama"]
        unique_together = ["creel", "sama"]

    def __str__(self):
        """return the object type, the interview log number (sama), the stratum,
        and project code of the creel this record is assoicated
       with.

        """

        repr = "<InterviewLog: {} ({})>"
        return repr.format(self.sama, self.creel.prj_cd)

    @property
    def dow(self):
        """Return the numeric day of the week of the interview log.
        Sunday=1, Saturday=7.

        Arguments:
        - `self`:
        """
        dow = int(datetime.strftime(self.date, "%w")) + 1
        return dow


#    @property
#    def daytype(self):
#        """get the day type associated with this interview log.  The day type
#        is determined by the creel, season, and date.  If a record
#        exsits for this date in the exception dates table (FN025) use it,
#        otherwise get the day type from the FN024 table.
#
#        Arguments:
#        - `self`:
#
#        """
#
#        #exception = FN025.objects.filter(season=self.season).\
#        #          filter(date=self.date).first()
#        #if exception:
#        #    daytype = FN023.objects.filter(season=self.season).\
#        #              filter(dtp=exception.dtp1).get()
#        #else:
#        #    daytype = FN023.objects.filter(season=self.season).\
#        #              filter(dow_lst__contains=self.dow).get()
#        #return daytype
#        return self.stratum.daytype.dtp
#
#    @property
#    def period(self):
#        """get the period associated with this interview log.  The period is
#        determined by the creel, season, date, and start time.
#
#        Arguments:
#        - `self`:
#
#        """
#        #period = FN024.objects.filter(daytype=self.daytype).\
#        #      filter(prdtm0__lte=self.samtm0).\
#        #      order_by('-prdtm0').first()
#        #return period
#        return self.stratum.period.prd
#
#    @property
#    def season(self):
#        """Given the project_code and date, return the corresponding season
#        for this creel log by finding the season that has start and
#        end dates span the date of the creel log.
#
#        Arguments:
#        - `self`:
#
#        """
#
#        #mydate = self.date.date()
#        #ssn = FN022.objects.filter(creel=self.creel).\
#        #      filter(ssn_date0__lte=mydate).\
#        #      filter(ssn_date1__gte=mydate).get()
#        #
#        #return ssn
#        return self.stratum.season.ssn
#
#    @property
#    def stratum(self):
#        """the stratum method should return the space, mode, day type,
#        period and season of an interview log, as a FishNet-2 stratum
#        string of the form: "XX_XX_XX_XX (SSN_[DayType][Period]_Area_Mode)."
#
#        """
##        myseason=self.season.ssn
##        myspace = self.area.space
##        myperiod = self.period.prd
##        mydaytype = self.daytype.dtp
##        mymode = self.mode.mode
##
##        repr = '{}_{}{}_{}_{}'.format(myseason, mydaytype, myperiod,
##                                      myspace, mymode)
##        return repr
#
#        return self.stratum.stratum


class FN112(models.Model):
    """Class to represent the activity counts associated with a creel log.
    """

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

    class Meta:
        verbose_name = "Activity Count"
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
        """from:http://stackoverflow.com/questions/7971689/
             generate-slug-field-in-existing-table

        Create a space label as a combination of the space description
        and space code.
        """

        # to calculate the difference between times, we need to convert
        # them to date.  Use the current date, it won't affect the results
        anydate = datetime.now().date()
        delta = datetime.combine(anydate, self.atytm1) - datetime.combine(
            anydate, self.atytm0
        )

        self.atydur = delta.total_seconds() / (60 * 60)
        super(FN112, self).save(*args, **kwargs)


class FN121(models.Model):
    """Class to represent the creel intervews.
    """

    # creel = models.ForeignKey(FN011, related_name='interviews')
    sama = models.ForeignKey(FN111, related_name="interviews", on_delete=models.CASCADE)

    # area = models.ForeignKey(FN026, related_name='interviews')
    # mode = models.ForeignKey(FN028, related_name='interviews')

    sam = models.CharField(max_length=6)
    itvseq = models.IntegerField()
    itvtm0 = models.TimeField(help_text="Interview Time")
    date = models.DateField()
    efftm0 = models.TimeField(help_text="Fishing Start Time")
    efftm1 = models.TimeField(blank=True, null=True, help_text="Fishing End Time")
    effcmp = models.BooleanField(default=False)
    effdur = models.FloatField(blank=True, null=True)
    persons = models.IntegerField(blank=True, null=True)
    anglers = models.IntegerField(blank=True, null=True)
    rods = models.IntegerField(blank=True, null=True)
    angmeth = models.IntegerField(blank=True, null=True)
    angvis = models.IntegerField(blank=True, null=True)
    angorig = models.IntegerField(blank=True, null=True)
    angop1 = models.CharField(max_length=25, blank=True, null=True)
    angop2 = models.CharField(max_length=25, blank=True, null=True)
    angop3 = models.CharField(max_length=25, blank=True, null=True)

    comment1 = models.TextField(blank=False, null=True)

    class Meta:
        verbose_name = "Inveriew"
        ordering = ["sama__creel__prj_cd", "sam"]
        # unique_together = ['sama__creel_id', 'sam']

    def __str__(self):
        """return the object type, the interview log number (sama), the stratum,
        and project code of the creel this record is assoicated
       with.

        """

        repr = "<Interview: {} ({})>"
        return repr.format(self.sam, self.sama.creel.prj_cd)


class FN123(models.Model):
    """Class to represent the creel catch counts.
    """

    interview = models.ForeignKey(
        FN121, related_name="catch_counts", on_delete=models.CASCADE
    )
    species = models.ForeignKey(
        Species, related_name="catch_counts", on_delete=models.CASCADE
    )
    sek = models.BooleanField(default=True)
    hvscnt = models.IntegerField(default=0)
    rlscnt = models.IntegerField(default=0)
    mescnt = models.IntegerField(default=0)
    meswt = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Catch"
        ordering = ["interview", "species"]
        unique_together = ["interview", "species"]

    def __str__(self):
        """return the object type, the interview log number (sama), the stratum,
        and project code of the creel this record is assoicated
       with.

        """
        repr = "<Catch: {}-{}-{}>"
        return repr.format(
            self.interview.stratum.creel.prj_cd,
            self.interview.sam,
            self.species.species_code,
        )


class FN125(models.Model):
    """Class to represent the attributes of sampled fish..
    """

    SEX_CHOICES = ((1, "Male"), (2, "Female"), (9, "Unknown"))

    MAT_CHOICES = ((1, "Immature"), (2, "Mature"), (9, "Unknown"))

    # get from FN_Dict.
    # GON_CHOICES = (
    # )

    catch = models.ForeignKey(
        FN123, related_name="bio_samples", on_delete=models.CASCADE
    )
    # species = models.ForeignKey(Species)

    grp = models.CharField(max_length=2)
    fish = models.IntegerField()
    flen = models.IntegerField(blank=True, null=True)
    tlen = models.IntegerField(blank=True, null=True)
    rwt = models.IntegerField(blank=True, null=True)
    sex = models.IntegerField(choices=SEX_CHOICES, default=None, blank=True, null=True)
    # gon should be a choice field too
    gon = models.CharField(max_length=2, blank=True, null=True)
    mat = models.IntegerField(choices=MAT_CHOICES, default=None, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    agest = models.CharField(max_length=8, blank=True, null=True)
    clipc = models.CharField(max_length=6, blank=True, null=True)
    fate = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        verbose_name = "Fish"
        ordering = ["catch", "fish"]
        unique_together = ["catch", "grp", "fish"]

    def __str__(self):
        """return the object type (fish), and the fishnet key fields prj_cd,
        sam, grp, spc and fish.

        """
        repr = "<Fish: {}-{}-{}-{}-{}>"
        return repr.format(
            self.catch.interview.stratum.creel.prj_cd,
            self.catch.interview.sam,
            self.catch.species.species_code,
            self.grp,
            self.fish,
        )


class FN127(models.Model):
    """Class to represent the attributes of and age estimate for a
    particular fish.

    """

    fish = models.ForeignKey(
        FN125, related_name="age_estimates", on_delete=models.CASCADE
    )

    ageid = models.IntegerField()
    agea = models.IntegerField(blank=True, null=True)
    agemt = models.CharField(max_length=6)
    conf = models.IntegerField(blank=True, null=True)
    edge = models.CharField(max_length=2, blank=True, null=True)
    nca = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "AgeEstimate"
        ordering = ["fish", "ageid"]
        unique_together = ["fish", "ageid"]

    def __str__(self):
        """return the object type (fish), and the fishnet key fields prj_cd,
        sam, grp, spc and fish.

        """
        repr = "<AgeEstimate: {}-{}-{}-{}-{}-{}>"
        return repr.format(
            self.fish.catch.interview.stratum.creel.prj_cd,
            self.fish.catch.interview.sam,
            self.fish.catch.species.species_code,
            self.fish.grp,
            self.fish.fish,
            self.ageid,
        )


class FR712(models.Model):
    """This table contains all of the strata attributes - the number of
    day and hours in each strata, the number of days and hours sampled,
    and the period duration.

    NOTE: This table should probably be merged with Strata and Strata
    removed.

    """

    REC_TP_CHOICES = ((1, "creel log (daily)"), (2, "stratum"), (3, "multi-stratum"))

    ATYUNIT_CHOICES = ((1, "Person"), (2, "Party"))

    CHKFLAG_CHOICES = ((0, "No"), (1, "Yes"))

    stratum = models.OneToOneField(
        Strata, on_delete=models.CASCADE, related_name="strata_values"
    )
    rec_tp = models.IntegerField(default=2, choices=REC_TP_CHOICES)
    strat_days = models.IntegerField()
    strat_hours = models.FloatField()
    sam_days = models.IntegerField(default=0, blank=True, null=True)
    sam_hours = models.FloatField(default=0, blank=True, null=True)
    fpc = models.FloatField(default=0)
    prd_dur = models.FloatField()
    atyunit = models.IntegerField(
        default=2, choices=ATYUNIT_CHOICES, blank=True, null=True
    )
    chkflag = models.IntegerField(
        default=1, choices=CHKFLAG_CHOICES, blank=True, null=True
    )
    strat1 = models.CharField(blank=True, null=True, max_length=11)
    strat_nn = models.IntegerField(default=1)

    def __str__(self):
        """return the object type (stratum values), the stratum lable, the
        creel project code and run number

        """
        repr = "<Stratum Values: {} ({}, run:{}))>"
        return repr.format(
            self.stratum.stratum_label,
            self.stratum.creel_run__creel__prj_cd,
            self.stratum.creel_run__run,
        )


class FR713(models.Model):
    """Class to hold creel estimate of effort by strata.

    TODO - figure out if we need strat, if it should be build
    dynamically or ahead of time or if a '++' placeholder should be
    created add to each stratum of each creel to represent the
    collapsed 'all' estimate.

    """

    stratum = models.ForeignKey(
        Strata, related_name="effort_estimates", on_delete=models.CASCADE
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
    run = models.CharField(max_length=2, db_index=True)
    rec_tp = models.IntegerField(default=1)
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
        verbose_name = "EffortEstimate"
        ordering = [
            "stratum__creel_run__creel__prj_cd",
            "run",
            "stratum__stratum_label",
            "date",
            "rec_tp",
        ]
        unique_together = ["stratum", "date", "rec_tp", "run"]

    def __str__(self):
        """return the object type (EffortEstimate), and the prj_cd.
        """
        repr = "<EffortEstimate: {} (run:{} strat:{})>"
        return repr.format(
            self.stratum.creel_run.creel.prj_cd,
            self.stratum.creel_run.run,
            self.stratum.stratum_label,
        )


class FR714(models.Model):
    """Class to hold creel estimate of harvest by strata and species.

    TODO - figure out if we need strat, if it should be build
    dynamically or ahead of time or if a '++' placeholder should be
    created add to each stratum of each creel to represent the
    collapsed 'all' estimate.

    """

    stratum = models.ForeignKey(
        Strata, related_name="catch_estimates", on_delete=models.CASCADE
    )
    species = models.ForeignKey(
        Species, related_name="catch_estimates", on_delete=models.CASCADE
    )

    #    creel = models.ForeignKey(FN011, related_name='catch_estimates')
    #
    #    season = models.ForeignKey(FN022, related_name='catch_estimates',
    #                              blank=True, null=True)
    #    dtp = models.ForeignKey(FN023, related_name='catch_estimates',
    #                            blank=True, null=True)
    #    period = models.ForeignKey(FN024, related_name='catch_estimates',
    #                               blank=True, null=True)
    #    area = models.ForeignKey(FN026, related_name='catch_estimates',
    #                             blank=True, null=True)
    #    mode = models.ForeignKey(FN028, related_name='catch_estimates',
    #                             blank=True, null=True)

    # NEW
    # run should be a fk to FR111 table
    run = models.CharField(max_length=2, db_index=True)
    rec_tp = models.IntegerField()
    # strat = models.CharField(max_length=11)
    date = models.DateField(blank=False, null=True)
    sek = models.BooleanField()
    cif1_nn = models.IntegerField()

    angler1_s = models.IntegerField()
    rod1_s = models.IntegerField()
    mescnt_s = models.IntegerField(blank=True, null=True)
    meswt_s = models.FloatField(blank=True, null=True)

    catne1 = models.FloatField()
    catne1_pc = models.FloatField(blank=True, null=True)
    catne1_se = models.FloatField()
    catne1_vr = models.FloatField(blank=True, null=True)

    catne = models.FloatField()
    catne_se = models.FloatField()
    catne_vr = models.FloatField(blank=True, null=True)

    catno1_s = models.IntegerField()
    catno1_ss = models.IntegerField(blank=True, null=True)
    catno_s = models.IntegerField()
    catno_ss = models.IntegerField(blank=True, null=True)

    effae1 = models.FloatField()
    effae1_pc = models.FloatField(blank=True, null=True)
    effae1_se = models.FloatField()
    effae1_vr = models.FloatField(blank=True, null=True)

    effao1_s = models.FloatField()
    effao1_ss = models.FloatField(blank=True, null=True)

    effpe1 = models.FloatField()
    effpe1_se = models.FloatField(blank=True, null=True)
    effpe1_vr = models.FloatField(blank=True, null=True)

    effpo1_s = models.FloatField(blank=True, null=True)
    effpo1_ss = models.FloatField(blank=True, null=True)

    effre1 = models.FloatField()
    effre1_se = models.FloatField()
    effre1_vr = models.FloatField(blank=True, null=True)

    effro1_s = models.FloatField()
    effro1_ss = models.FloatField(blank=True, null=True)

    hvscat_pc = models.FloatField()

    hvsne = models.FloatField()
    hvsne_se = models.FloatField()
    hvsne_vr = models.FloatField(blank=True, null=True)

    hvsne1 = models.FloatField()
    hvsne1_se = models.FloatField()
    hvsne1_vr = models.FloatField(blank=True, null=True)

    cuenao = models.FloatField()
    cuenao1 = models.FloatField(blank=True, null=True)
    cuenae = models.FloatField()
    cuenae1 = models.FloatField(blank=True, null=True)

    hvsno_s = models.IntegerField()
    hvsno_ss = models.IntegerField(blank=True, null=True)

    hvsno1_s = models.IntegerField()
    hvsno1_ss = models.IntegerField(blank=True, null=True)

    catea_xy = models.FloatField(blank=True, null=True)
    catea1_xy = models.FloatField(blank=True, null=True)
    hvsea_xy = models.FloatField(blank=True, null=True)
    hvsea1_xy = models.FloatField(blank=True, null=True)
    cater_xy = models.FloatField(blank=True, null=True)
    cater1_xy = models.FloatField(blank=True, null=True)
    hvser_xy = models.FloatField(blank=True, null=True)
    hvser1_xy = models.FloatField(blank=True, null=True)
    catep_xy = models.FloatField(blank=True, null=True)
    catep1_xy = models.FloatField(blank=True, null=True)
    hvsep_xy = models.FloatField(blank=True, null=True)
    hvsep1_xy = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "HarvestEstimate"
        ordering = [
            "stratum__creel_run__creel__prj_cd",
            "stratum__creel_run__run",
            "stratum__stratum_label",
            "species",
            "date",
            "rec_tp",
            "sek",
        ]
        unique_together = ["stratum", "species", "date", "rec_tp", "sek", "run"]

    def __str__(self):
        """return the object type (EffortEstimate), and the prj_cd."""

        repr = "<HarvestEstimate: {} ({} run:{} strat:{} sek:{})>"

        targetted = "Targetted" if self.sek else "NonTargetted"
        return repr.format(
            self.species.species_code,
            self.stratum.creel_run.creel.prj_cd,
            self.stratum.creel_run.run,
            self.stratum.stratum_label,
            targetted,
        )
