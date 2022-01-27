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
from django.template.defaultfilters import slugify

import json

from common.models import Species


class FN121(models.Model):
    """Class to represent the creel intervews."""

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
        app_label = "creel_portal"
        verbose_name = "FN121 - Inveriew"
        ordering = ["sama__creel__prj_cd", "sam"]
        # unique_together = ['sama__creel_id', 'sam']

    def save(self, *args, **kwargs):
        """ """

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
    """Class to represent the creel catch counts."""

    interview = models.ForeignKey(
        FN121, related_name="catch_counts", on_delete=models.CASCADE
    )
    species = models.ForeignKey(
        Species, related_name="sc_catch_counts", on_delete=models.CASCADE
    )

    grp = models.CharField(max_length=3, default="00", db_index=True)
    sek = models.BooleanField(default=True)
    hvscnt = models.IntegerField(default=0)
    rlscnt = models.IntegerField(default=0)
    mescnt = models.IntegerField(default=0)
    meswt = models.FloatField(blank=True, null=True)

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN123 - Catch Count"
        ordering = ["interview", "species"]
        unique_together = ["interview", "grp", "species"]

    def save(self, *args, **kwargs):
        """ """

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
    """Class to represent the attributes of sampled fish.."""

    SEX_CHOICES = ((1, "Male"), (2, "Female"), (3, "Hermaphrodite"), (9, "Unknown"))
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
        app_label = "creel_portal"
        verbose_name = "FN125 - Bio Sample"
        ordering = ["catch", "fish"]
        unique_together = ["catch", "fish"]

    def save(self, *args, **kwargs):
        """ """

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
    """a table for lamprey data."""

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
        app_label = "creel_portal"
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
    """a table for the tag(s) assoicated with a fish."""

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
        app_label = "creel_portal"
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
    """a table for diet data collected in the field."""

    fish = models.ForeignKey(FN125, related_name="diet_data", on_delete=models.CASCADE)
    slug = models.CharField(max_length=100, unique=True)
    food = models.IntegerField()

    taxon = models.CharField(
        "A taxonomic code used to identify the type of food item.",
        max_length=10,
        db_index=True,
        blank=True,
        null=True,
    )
    foodcnt = models.IntegerField("Food Count", blank=True, null=True)
    foodval = models.FloatField("Food Measure Value", blank=True, null=True)

    FDMES_CHOICES = (
        (None, "No Data"),
        ("L", "Length"),
        ("W", "Weight"),
        ("V", "Volume"),
    )
    fdmes = models.CharField(
        help_text="Food Measure Code",
        max_length=2,
        blank=True,
        choices=FDMES_CHOICES,
    )

    LIFESTAGE_CHOICES = (
        (None, "No Data"),
        ("10", "10"),
        ("20", "20"),
        ("30", "30"),
        ("40", "40"),
        ("50", "50"),
        ("60", "60"),
    )
    lf = models.CharField(
        help_text="Life Stage",
        max_length=2,
        blank=True,
        choices=LIFESTAGE_CHOICES,
    )

    comment6 = models.TextField(blank=True, null=True)

    class Meta:
        app_label = "creel_portal"
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

    agea = models.IntegerField(
        "Age Assessed (yr)", blank=True, null=True, db_index=True
    )
    agemt = models.CharField("Age Method Data", max_length=6)
    edge = models.CharField("Edge Code", max_length=2, blank=True, null=True)
    conf = models.IntegerField("Confidence", blank=True, null=True)
    nca = models.IntegerField("Number of Complete Annuli", blank=True, null=True)

    preferred = models.BooleanField(
        "Preferred age estimate for a fish", default=False, db_index=True
    )
    agest = models.CharField(
        "Age Structure", max_length=5, db_index=True, blank=True, null=True
    )

    ageaDate = models.DateTimeField(blank=True, null=True)
    comment7 = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN127 - AgeEstimate"
        ordering = ["fish", "ageid"]
        unique_together = ["fish", "ageid"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN127, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.fish, self.ageid)

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
