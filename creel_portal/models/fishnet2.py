"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/creel_portal/creel_portal/models/FishNet2.py
 Created: 30 Mar 2020 08:39:05

 DESCRIPTION:

  This file contains all of the standard tables from a fishnet-II project:

+ FN011
+ FN121
+ FN122 (omitted for creels)
+ FN123
+ FN124 (omitted for creels)
+ FN125
+ FN125_Tags
+ FN125_Lamprey
+ FN126
+ FN127

TODO: Create a FishNet2 Django Application that contains nothing but
abstract base classes for these models that other project types inherit from.


 A. Cottrill
=============================================================

"""

from django.db import models
from django.db.models import Sum, F
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse

import json

from common.models import Lake, Species


from .choices import CONTMETH_CHOICES


User = get_user_model()


# note = move this to main.models too
class FN011(models.Model):
    """Class to hold a record for each project
    """

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
        verbose_name = "FN011 - Creel"
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


class FN121(models.Model):
    """Class to represent the creel intervews.
    """

    # creel = models.ForeignKey(FN011, related_name='interviews')
    sama = models.ForeignKey(
        "FN111", related_name="interviews", on_delete=models.CASCADE
    )

    slug = models.SlugField(blank=True, unique=True, editable=False)

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
        verbose_name = "FN121 - Inveriew"
        ordering = ["sama__creel__prj_cd", "sam"]
        # unique_together = ['sama__creel_id', 'sam']

    def save(self, *args, **kwargs):
        """
        """

        raw_slug = "-".join([self.sama.creel.prj_cd, self.sam])

        self.slug = slugify(raw_slug)
        super(FN121, self).save(*args, **kwargs)

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
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    grp = models.CharField(max_length=3, default="00", db_index=True)
    sek = models.BooleanField(default=True)
    hvscnt = models.IntegerField(default=0)
    rlscnt = models.IntegerField(default=0)
    mescnt = models.IntegerField(default=0)
    meswt = models.FloatField(blank=True, null=True)

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        verbose_name = "FN123 - Catch Count"
        ordering = ["interview", "species"]
        unique_together = ["interview", "grp", "species"]

    def save(self, *args, **kwargs):
        """
        """

        raw_slug = "-".join(
            [
                self.interview.sama.creel.prj_cd,
                self.interview.sam,
                self.grp,
                self.species.spc,
            ]
        )

        self.slug = slugify(raw_slug)
        super(FN123, self).save(*args, **kwargs)

    def __str__(self):
        """return the object type, the interview log number (sama), the stratum,
        and project code of the creel this record is assoicated
       with.

        """
        repr = "<Catch: {}-{}-{}-{}>"
        return repr.format(
            self.interview.sama.creel.prj_cd,
            self.interview.sam,
            self.grp,
            self.species.spc,
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

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        verbose_name = "FN125 - Bio Sample"
        ordering = ["catch", "fish"]
        unique_together = ["catch", "fish"]

    def save(self, *args, **kwargs):
        """
        """

        raw_slug = "-".join(
            [
                self.catch.interview.sama.creel.prj_cd,
                self.catch.interview.sam,
                self.catch.species.spc,
                self.catch.grp,
                str(self.fish),
            ]
        )

        self.slug = slugify(raw_slug)
        super(FN125, self).save(*args, **kwargs)

    def __str__(self):
        """return the object type (fish), and the fishnet key fields prj_cd,
        sam, grp, spc and fish.

        """
        repr = "<Fish: {}-{}-{}-{}-{}>"
        return repr.format(
            self.catch.interview.sama.creel.prj_cd,
            self.catch.interview.sam,
            self.catch.species.spc,
            self.catch.grp,
            self.fish,
        )


class FN125_Lamprey(models.Model):
    """ a table for lamprey data. """

    fish = models.ForeignKey(
        FN125, related_name="lamprey_marks", on_delete=models.CASCADE
    )
    slug = models.CharField(max_length=100, unique=True)
    lamid = models.IntegerField()
    xlam = models.CharField(max_length=6, blank=True, null=True)
    lamijc = models.CharField(max_length=50, blank=True, null=True)

    LAMIJC_TYPE_CHOICES = (
        ["0", "0"],
        ["a1", "A1"],
        ["a2", "A2"],
        ["a3", "A3"],
        ["a4", "A4"],
        ["b1", "B1"],
        ["b2", "B2"],
        ["b3", "B3"],
        ["b4", "B4"],
    )
    lamijc_type = models.CharField(
        max_length=2, choices=LAMIJC_TYPE_CHOICES, default="0"
    )

    lamijc_size = models.IntegerField(blank=True, null=True)
    comment_lam = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["slug", "lamid"]

    # unique_together = ('fish', 'tagnum', 'grp')

    def __str__(self):

        if self.xlam:
            return "{} (xlam: {})".format(self.slug.upper(), self.xlam)
        else:
            return "{} (lamijc: {})".format(self.slug.upper(), self.lamijc)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN125_Lamprey, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        repr = "{}-{}-{}-{}-{}-{}"

        return repr.format(
            self.fish.catch.interview.sama.creel.prj_cd,
            self.fish.catch.interview.sam,
            self.fish.catch.species.spc,
            self.fish.catch.grp,
            self.fish.fish,
            self.lamid,
        )


class FN125_Tag(models.Model):
    """ a table for the tag(s) assoicated with a fish.
    """

    fish = models.ForeignKey(FN125, related_name="fishtags", on_delete=models.CASCADE)
    slug = models.CharField(max_length=100, unique=True)
    fish_tag_id = models.IntegerField()
    # tag fields
    tagstat = models.CharField(max_length=5, db_index=True, blank=True, null=True)
    tagid = models.CharField(max_length=9, blank=True, null=True)
    tagdoc = models.CharField(max_length=6, db_index=True, blank=True, null=True)
    xcwtseq = models.CharField(max_length=5, blank=True, null=True)
    xtaginckd = models.CharField(max_length=6, blank=True, null=True)
    xtag_chk = models.CharField(max_length=50, blank=True, null=True)

    comment_tag = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["fish", "fish_tag_id"]
        unique_together = ("fish", "fish_tag_id")

    def __str__(self):
        return "{} ({} ({}))".format(self.slug.upper(), self.tagid, self.tagdoc)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN125_Tag, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""

        repr = "{}-{}-{}-{}-{}-{}"

        return repr.format(
            self.fish.catch.interview.sama.creel.prj_cd,
            self.fish.catch.interview.sam,
            self.fish.catch.species.spc,
            self.fish.catch.grp,
            self.fish.fish,
            self.fish_tag_id,
        )


class FN126(models.Model):
    """ a table for diet data collected in the field.
    """

    fish = models.ForeignKey(FN125, related_name="diet_data", on_delete=models.CASCADE)
    slug = models.CharField(max_length=100, unique=True)
    food = models.IntegerField()

    taxon = models.CharField(max_length=10, db_index=True, blank=True, null=True)
    foodcnt = models.IntegerField(blank=True, null=True)
    comment6 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["fish", "food"]
        unique_together = ("fish", "food")

    def __str__(self):
        return "{} ({}: {})".format(self.slug.upper(), self.taxon, self.foodcnt)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN126, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.fish, self.food)


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
        verbose_name = "FN127 - AgeEstimate"
        ordering = ["fish", "ageid"]
        unique_together = ["fish", "ageid"]

    def __str__(self):
        """return the object type (fish), and the fishnet key fields prj_cd,
        sam, grp, spc and fish.

        """
        repr = "<AgeEstimate: {}-{}-{}-{}-{}-{}>"

        return repr.format(
            self.fish.catch.interview.sama.creel.prj_cd,
            self.fish.catch.interview.sam,
            self.fish.catch.species.spc,
            self.fish.catch.grp,
            self.fish.fish,
            self.ageid,
        )
