"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/creel_portal/creel_portal/models/FishNet2.py
 Created: 30 Mar 2020 08:39:05

 DESCRIPTION:

  This file contains all of the standard tables from a fishnet-II project:

TODO: Create a FishNet2 Django Application that contains nothing but
abstract base classes for these models that other project types inherit from.


 A. Cottrill
=============================================================

"""

from django.db import models
from django.template.defaultfilters import slugify

from common.models import Species


class FN123(models.Model):
    """Class to represent the creel catch counts."""

    interview = models.ForeignKey(
        "FN121", related_name="catch_counts", on_delete=models.CASCADE
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
