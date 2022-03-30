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

from .choices import FDMES_CHOICES, LIFESTAGE_CHOICES


class FN126(models.Model):
    """a table for diet data collected in the field."""

    fish = models.ForeignKey(
        "FN125", related_name="diet_data", on_delete=models.CASCADE
    )
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

    fdmes = models.CharField(
        help_text="Food Measure Code",
        max_length=2,
        blank=True,
        choices=FDMES_CHOICES,
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
