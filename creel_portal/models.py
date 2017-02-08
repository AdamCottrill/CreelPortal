from django.db import models

from django.template.defaultfilters import slugify

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

    class Meta:
        verbose_name = "Creel List"
        ordering = ['-prj_date1']


    ##  aru
    ##  fof_loc
    ##  fof_nm
    ##  prj_his
    ##  prj_size
    ##  prj_ver
    ##
    ##  wby
    ##  wby_nm
    ##  v0

        #@models.permalink
    #    def get_absolute_url(self):
    #        '''return the url for the project'''
    #        url = reverse('creel_portal.views.creel_detail',
    #                      kwargs={'slug':self.slug})
    #        return url
    #


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
