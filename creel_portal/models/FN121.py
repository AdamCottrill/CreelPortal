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
from django.template.defaultfilters import slugify

from .choices import ANGMETH_CHOICES, ANGVIZ_CHOICES, ANGORIG_CHOICES


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
    angmeth = models.IntegerField(blank=True, null=True, choices=ANGMETH_CHOICES)
    angvis = models.IntegerField(blank=True, null=True, choices=ANGVIZ_CHOICES)
    angorig = models.IntegerField(blank=True, null=True, choices=ANGORIG_CHOICES)
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
