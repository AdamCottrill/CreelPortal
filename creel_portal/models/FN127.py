"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/creel_portal/creel_portal/models/FishNet2.py
 Created: 30 Mar 2020 08:39:05

 DESCRIPTION:

 This file contains all of the standard tables from a fishnet-II project:

 + FN127

  TODO: Create a FishNet2 Django Application that contains nothing but
  abstract base classes for these models that other project types inherit from.

 A. Cottrill
=============================================================

"""

from django.db import models
from django.template.defaultfilters import slugify


class FN127(models.Model):
    """Class to represent the attributes of and age estimate for a
    particular fish.

    """

    fish = models.ForeignKey(
        "FN125", related_name="age_estimates", on_delete=models.CASCADE
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
