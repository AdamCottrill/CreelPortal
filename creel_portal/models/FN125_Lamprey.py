"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/creel_portal/creel_portal/models/FishNet2.py
 Created: 30 Mar 2020 08:39:05

 DESCRIPTION:

  This file contains all of the standard tables from a fishnet-II project:

  + FN125_Lamprey

  TODO: Create a FishNet2 Django Application that contains nothing but
  abstract base classes for these models that other project types inherit from.

 A. Cottrill
=============================================================

"""

from django.db import models
from django.template.defaultfilters import slugify

from .choices import LAMIJC_TYPE_CHOICES


class FN125_Lamprey(models.Model):
    """a table for lamprey data."""

    fish = models.ForeignKey(
        "FN125", related_name="lamprey_marks", on_delete=models.CASCADE
    )
    slug = models.CharField(max_length=100, unique=True)
    lamid = models.IntegerField()
    xlam = models.CharField(max_length=6, blank=True, null=True)
    lamijc = models.CharField(max_length=50, blank=True, null=True)

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
