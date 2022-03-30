"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/creel_portal/creel_portal/models/FishNet2.py
 Created: 30 Mar 2020 08:39:05

 DESCRIPTION:

  This file contains all of the standard tables from a fishnet-II project:

  + FN125

  TODO: Create a FishNet2 Django Application that contains nothing but
  abstract base classes for these models that other project types inherit from.


 A. Cottrill
=============================================================

"""

from django.db import models
from django.template.defaultfilters import slugify

from .choices import SEX_CHOICES, MAT_CHOICES


class FN125(models.Model):
    """Class to represent the attributes of sampled fish.."""

    # get from FN_Dict.
    # GON_CHOICES = (
    # )

    catch = models.ForeignKey(
        "FN123", related_name="bio_samples", on_delete=models.CASCADE
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
    # age = models.IntegerField(blank=True, null=True)
    agest = models.CharField(max_length=8, blank=True, null=True)
    clipc = models.CharField(max_length=6, blank=True, null=True)
    tissue = models.CharField(max_length=20, blank=True, null=True)
    fate = models.CharField(max_length=2, blank=True, null=True)

    # flags for child tables:
    age_flag = models.BooleanField(default=False)
    stom_flag = models.BooleanField(default=False)
    lam_flag = models.BooleanField(default=False)
    tag_flag = models.BooleanField(default=False)

    comment5 = models.CharField(max_length=500, blank=True, null=True)

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
