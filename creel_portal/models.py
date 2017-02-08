from django.db import models

from django.template.defaultfilters import slugify

from datetime import datetime

# Create your models here.


class Lake(models.Model):
    '''A lookup table to hold the names of the different lakes'''

    abbrev = models.CharField(max_length=10, unique=True)
    lake_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Lake"

    def __str__(self):
        '''return the lake name as its string representation'''
        return "<Lake: {} ({})>".format(self.lake_name, self.abbrev)


class FN011(models.Model):
    '''Class to hold a record for each project
    '''

    lake = models.ForeignKey(Lake, default=1)

    prj_date0 = models.DateField("Start Date", blank=False)
    prj_date1 = models.DateField("End Date", blank=False)
    prj_cd = models.CharField("Project Code", max_length=12, unique=True,
                              blank=False)
    year = models.CharField("Year", max_length=4, blank=True, editable=False)
    prj_nm = models.CharField("Project Name", max_length=60, blank=False)
    prj_ldr = models.CharField("Project Lead", max_length=40, blank=False)
    comment0 = models.TextField(blank=False,
                               help_text="General project description.")
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
        super(Project, self).save( *args, **kwargs)


class FN022(models.Model):
    '''Class to represent the seasons (temporal strata) used in each creel.
    '''

    creel = models.ForeignKey(FN011)
    ssn = models.CharField("Season Code", max_length=2, blank=False)
    ssn_des = models.CharField("Season Description", max_length=60,
                               blank=False)
    ssn_date0 = models.DateField("Season Start Date", blank=False)
    ssn_date1 = models.DateField("Season End Date", blank=False)
    v0 = models.CharField(max_length=4, blank=False)

    class Meta:
        verbose_name = "Seasons"
        ordering = ['ssn']

    def __str__(self):
        '''return the season name, code and project code associated with this
        particular season.'''

        repr =  "<Season: {} ({}) [{}]>"
        return repr.format(self.ssn_des, self.ssn, self.creel.prj_cd)


class FN023(models.Model):
    '''Class  to represent the daytypes used in each season of creel
    '''

    season = models.ForeignKey(FN022)
    dow_lst = models.CharField("DayOfWeek List", max_length=7, blank=False)
    dtp = models.CharField("Day Type Code", max_length=2,
                               blank=False)
    dtp_nm = models.CharField("Day Type Name", max_length=10,
                               blank=False)

    class Meta:
        verbose_name = "Day Types"
        ordering = ['dtp']

    def __str__(self):
        '''return the object type, the daytype name, day type code, and the
       code project code of the creel this record is assoicated with.

        '''

        repr =  "<DayType: {}({}) {}-{}>"
        return repr.format(self.dtp_nm, self.dtp, self.season.ssn,
                           self.season.creel.prj_cd)


class FN024(models.Model):
    '''Class to represent the period used in each day types of each season
    of creel.
    '''

    daytype = models.ForeignKey(FN023)
    prd = models.CharField("Day Type Code", max_length=2, blank=False)
    prdtm0 = models.TimeField("Period Start Time", blank=False)
    prdtm1 = models.TimeField("Period End Time", blank=False)

    class Meta:
        verbose_name = "Periods"
        ordering = ['prd']

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
    date = models.DateField("Exception Date", blank=False)
    dtp1 = models.CharField("Day Type Code", max_length=2,
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


#class FN026(models.Model):
#    '''Class to represent the spatial strat used in a creel.
#    '''
