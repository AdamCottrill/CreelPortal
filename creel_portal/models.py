from django.db import models

from django.template.defaultfilters import slugify

from datetime import datetime

# Create your models here.

#note = move this to main.models
class Species(models.Model):
    species_code = models.IntegerField(unique=True)
    common_name = models.CharField(max_length=30)
    scientific_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['species_code']

    def __str__(self):
        if self.scientific_name:
            spc_str = "<Species: %s (%s)>" % (self.common_name,
                                              self.scientific_name)
        else:
            spc_str = "<Species: %s>" % self.common_name
        return spc_str

#note = move this to main.models
class Lake(models.Model):
    '''A lookup table to hold the names of the different lakes'''

    abbrev = models.CharField(max_length=10, unique=True)
    lake_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Lake"

    def __str__(self):
        '''return the lake name as its string representation'''
        return "<Lake: {} ({})>".format(self.lake_name, self.abbrev)

#note = move this to main.models too
class FN011(models.Model):
    '''Class to hold a record for each project
    '''

    lake = models.ForeignKey(Lake, default=1)

    prj_date0 = models.DateField(help_text="Start Date", blank=False)
    prj_date1 = models.DateField(help_text="End Date", blank=False)
    prj_cd = models.CharField(help_text="Project Code", max_length=12,
                              unique=True, blank=False)
    year = models.CharField(help_text="Year", max_length=4, blank=True,
                            editable=False)
    prj_nm = models.CharField(help_text="Project Name", max_length=60,
                              blank=False)
    prj_ldr = models.CharField(help_text="Project Lead", max_length=40,
                               blank=False)
    comment0 = models.TextField(blank=False,
                               help_text="General Project Description.")
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
        ordering = ['-prj_date1']

        #@models.permalink
    #    def get_absolute_url(self):
    #        '''return the url for the project'''
    #        url = reverse('creel_portal.views.creel_detail',
    #                      kwargs={'slug':self.slug})
    #        return url
    #


    def __str__(self):
        '''return the creel name and project code as its string
        representation'''
        return "<Creel: {} ({})>".format(self.prj_nm, self.prj_cd)


    def save(self, *args, **kwargs):
        """
        from:http://stackoverflow.com/questions/7971689/
             generate-slug-field-in-existing-table
        Slugify name if it doesn't exist. IMPORTANT: doesn't check to see
        if slug is a dupicate!
        """
        new = False
        if not self.slug or not self.year:
            self.slug = slugify(self.prj_cd)
            self.year = self.prj_date0.year
            new = True
        super(FN011, self).save( *args, **kwargs)


class FN022(models.Model):
    '''Class to represent the seasons (temporal strata) used in each creel.
    '''

    creel = models.ForeignKey(FN011)
    ssn = models.CharField(help_text="Season Code", max_length=2, blank=False)
    ssn_des = models.CharField(help_text="Season Description", max_length=60,
                               blank=False)
    ssn_date0 = models.DateField(help_text="Season Start Date", blank=False)
    ssn_date1 = models.DateField(help_text="Season End Date", blank=False)
    v0 = models.CharField(max_length=4, blank=False)

    class Meta:
        verbose_name = "Seasons"
        ordering = ['ssn']
        unique_together = ['creel', 'ssn']

    def __str__(self):
        '''return the season name, code and project code associated with this
        particular season.'''

        repr =  "<Season: {} ({}) [{}]>"
        return repr.format(self.ssn_des, self.ssn, self.creel.prj_cd)


class FN023(models.Model):
    '''Class  to represent the daytypes used in each season of creel
    '''
    #creel = models.ForeignKey(FN011)
    season = models.ForeignKey(FN022)
    dtp = models.CharField(help_text="Day Type Code", max_length=2,
                              blank=False)
    dtp_nm = models.CharField(help_text="Day Type Name", max_length=10,
                               blank=False)
    dow_lst = models.CharField(help_text="Day Of Week List",
                               max_length=7, blank=False)

    class Meta:
        verbose_name = "Day Types"
        ordering = ['dtp']
        unique_together = ['season', 'dtp']

    def __str__(self):
        '''return the object type, the daytype name, day type code, and the
       code project code of the creel this record is assoicated with.

        '''

        repr =  "<DayType: {}({}) {}-{}>"
        return repr.format(self.dtp_nm, self.dtp, self.season.ssn,
                           self.season.creel.prj_cd)
        #repr =  "<DayType: {}({}) [{}]>"
        #return repr.format(self.dtp_nm, self.dtp,
        #                   self.creel.prj_cd)


class FN024(models.Model):
    '''Class to represent the period used in each day types of each season
    of creel.
    '''

    daytype = models.ForeignKey(FN023)
    prd = models.CharField(help_text="Day Type Code", max_length=2, blank=False)
    prdtm0 = models.TimeField(help_text="Period Start Time", blank=False)
    prdtm1 = models.TimeField(help_text="Period End Time", blank=False)

    class Meta:
        verbose_name = "Periods"
        ordering = ['prd']
        unique_together = ['daytype', 'prd']

    def __str__(self):
        '''return the object type, period code, the daytype name, the season,
       and project code of the creel this record is assoicated with.

        '''

        start = self.prdtm0.strftime("%H:%M")
        end = self.prdtm1.strftime("%H:%M")

        repr =  "<Period: {}({}-{}) {}-{}-{}>"
        return repr.format(self.prd, start, end,
                           self.daytype.dtp_nm, self.daytype.season.ssn_des,
                           self.daytype.season.creel.prj_cd)


class FN025(models.Model):
    '''Class to represent the day type exceptions so that holidays can be
    treated as weekends.
    '''

    season = models.ForeignKey(FN022)
    date = models.DateField(help_text="Exception Date", blank=False)
    dtp1 = models.CharField(help_text="Day Type Code", max_length=2,
                               blank=False)

    class Meta:
        verbose_name = "Exception Dates"
        ordering = ['date']


#    def get_dtp_nm(self):
#        """the day types are stored in the FN023 table.  We want to return
#        dpt_nm from FN023 where the season and dpt match."""
#
#        dtp_nm = FN023.objects.filter(season=self.season,
#                                      dtp=self.dpt1).values('dpt_name')[0]
#        return dpt_nm

    def __str__(self):
        '''return the object type, the date, the season name, and
       code project code of the creel this record is assoicated with.

        '''
        fdate = datetime.strftime(self.date,'%Y-%m-%d')
        repr =  "<ExceptionDate: {} ({}-{})>"
        return repr.format(fdate, self.season.ssn_des,
                           self.season.creel.prj_cd)


class FN026(models.Model):
    '''Class to represent the spatial strat used in a creel.
    '''


    creel = models.ForeignKey(FN011)
    space = models.CharField(max_length=2, blank=False,
                             help_text="Space Code")
    space_des = models.CharField(max_length=100, blank=False,
                                 help_text= "Space Description",)
    space_siz = models.IntegerField(blank=True, null=True)
    area_cnt = models.IntegerField(blank=True, null=True)
    area_lst = models.CharField(max_length=2, help_text="Area List",
                                blank=True, null=True)
    area_wt = models.FloatField(blank=True, null=True)

    ddlat = models.FloatField(blank=True, null=True)
    ddlat = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Spatial Strata"
        ordering = ['space']
        unique_together = ['creel', 'space']

    def __str__(self):
        '''return the object type, the space name, the space code, and
       project code of the creel this record is assoicated with.

        '''

        repr =  "<Space: {} ({}) [{}]>"
        return repr.format(self.space_des, self.space,
                           self.creel.prj_cd)


class FN028(models.Model):
    '''Class to represent the fishing modes used in a creel.
    '''

    creel = models.ForeignKey(FN011)
    mode = models.CharField(help_text="Mode Code", max_length=2, blank=False)
    mode_des = models.CharField(help_text="Fishing Mode Description",
                                max_length=100, blank=False)
    atyunit = models.IntegerField(help_text="Activity Unit")
    itvunit = models.IntegerField(help_text="Interview Unit")
    chkflag = models.IntegerField(help_text="Check Flag")

    class Meta:
        verbose_name = "Fishing Mode"
        ordering = ['mode']
        unique_together = ['creel', 'mode']

    def __str__(self):
        '''return the object type, the mode name, the mode code, and
       project code of the creel this record is assoicated with.

        '''

        repr =  "<FishingMode: {} ({}) [{}]>"
        return repr.format(self.mode_des, self.mode,
                           self.creel.prj_cd)


class FN111(models.Model):
    '''Class to represent the creel logs.
    '''

    creel = models.ForeignKey(FN011)
    area = models.ForeignKey(FN026)
    mode = models.ForeignKey(FN028)

    sama = models.CharField(max_length=6, blank=False)
    date = models.DateField(blank=False)
    samtm0 = models.TimeField(blank=False,
                              help_text="Interview Period Start")
    weather = models.CharField(max_length=200, blank=False)
    help_str = 'Comments about current interview period.'
    comment1 = models.CharField(max_length=200, blank=False,
                                help_text=help_str)

    class Meta:
        verbose_name = "Inveriew Log"
        ordering = ['creel', 'sama']
        unique_together = ['creel', 'sama']

    def __str__(self):
        '''return the object type, the interview log number (sama), the stratum,
        and project code of the creel this record is assoicated
       with.

        '''

        repr =  "<InterviewLog: {} ({})>"
        return repr.format(self.sama, self.creel.prj_cd)

    @property
    def daytype(self):
        """get the day type associated with this interview log.  The day type
        is determined by the creel, season, and date.  If a record
        exsits for this date in the exception dates table (FN025) use it,
        otherwise get the day type from the FN024 table.

        Arguments:
        - `self`:

        """

        exception = FN025.objects.filter(season=self.season).\
                  filter(date=self.date).first()
        if exception:
            daytype = FN023.objects.filter(season=self.season).\
                      filter(dtp=exception.dtp1).get()
        else:
            daytype = FN023.objects.filter(season=self.season).\
                      filter(dow_lst__contains=self.dow).get()
        return daytype

    @property
    def period(self):
        """get the period associated with this interview log.  The period is
        determined by the creel, season, date, and start time.

        Arguments:
        - `self`:

        """
        period = FN024.objects.filter(daytype=self.daytype).\
              filter(prdtm0__lte=self.samtm0).\
              order_by('-prdtm0').first()
        return period

    @property
    def dow(self):
        """Return the numeric day of the week of the interview log.
        Sunday=1, Saturday=7.

        Arguments:
        - `self`:
        """
        dow = int(datetime.strftime(self.date, '%w')) + 1
        return dow


    @property
    def season(self):
        """Given the project_code and date, return the corresponding season
        for this creel log by finding the season that has start and
        end dates span the date of the creel log.

        Arguments:
        - `self`:

        """

        mydate = self.date.date()
        ssn = FN022.objects.filter(creel=self.creel).\
              filter(ssn_date0__lte=mydate).\
              filter(ssn_date1__gte=mydate).get()

        return ssn


    @property
    def stratum(self):
        """the stratum method should return the space, mode, day type,
        period and season of an interview log, as a FishNet-2 stratum
        string of the form: "XX_XX_XX_XX (SSN_[DayType][Period]_Area_Mode)."

        """
        myseason=self.season.ssn
        myspace = self.area.space
        myperiod = self.period.prd
        mydaytype = self.daytype.dtp
        mymode = self.mode.mode

        repr = '{}_{}{}_{}_{}'.format(myseason, mydaytype, myperiod,
                                      myspace, mymode)
        return repr



class FN121(models.Model):
    '''Class to represent the creel intervews.
    '''

    creel = models.ForeignKey(FN011)
    sama = models.ForeignKey(FN111)
    mode = models.ForeignKey(FN028)
    area = models.ForeignKey(FN026)

    sam = models.CharField(max_length=6)
    itvseq = models.IntegerField()
    itvtm0 = models.TimeField(help_text="Interview Time")
    date = models.DateField()
    efftm0 = models.TimeField(help_text="Fishing Start Time")
    efftm1 = models.TimeField(blank=True, null=True,
                              help_text="Fishing End Time")
    effcmp = models.BooleanField(default=False)
    effdur = models.FloatField(blank=True, null=True)
    persons = models.IntegerField(blank=True, null=True)
    anglers = models.IntegerField(blank=True, null=True)
    rods = models.IntegerField(blank=True, null=True)
    angmeth = models.IntegerField(blank=True, null=True)
    angvis = models.IntegerField(blank=True, null=True)
    angorig = models.IntegerField(blank=True, null=True)
    angop1 = models.IntegerField(blank=True, null=True)
    angop2 = models.IntegerField(blank=True, null=True)
    angop3 = models.IntegerField(blank=True, null=True)
    comment1 = models.TextField(blank=False, null=True)

    class Meta:
        verbose_name = "Inveriew"
        ordering = ['creel', 'sam']
        unique_together = ['creel', 'sam']

    def __str__(self):
        '''return the object type, the interview log number (sama), the stratum,
        and project code of the creel this record is assoicated
       with.

        '''

        repr =  "<Interview: {} ({})>"
        return repr.format(self.sam, self.creel.prj_cd)






class FN123(models.Model):
    '''Class to represent the creel catch counts.
    '''

    interview = models.ForeignKey(FN121)
    species = models.ForeignKey(Species)
    sek = models.BooleanField(default=True)
    hvscnt = models.IntegerField(default=0)
    rlscnt = models.IntegerField(default=0)
    mescnt = models.IntegerField(default=0)
    meswt = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Catch"
        ordering = ['interview', 'species']
        unique_together = ['interview', 'species']

    def __str__(self):
        '''return the object type, the interview log number (sama), the stratum,
        and project code of the creel this record is assoicated
       with.

        '''
        repr = "<Catch: {}-{}-{}>"
        return repr.format(self.interview.creel.prj_cd,
                           self.interview.sam,
                           self.species.species_code)
