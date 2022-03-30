"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/creel_portal/creel_portal/models/FishNet2.py
 Created: 30 Mar 2020 08:39:05

 DESCRIPTION:

 This file contains all of the standard tables from a fishnet-II project:

 + FN125_Tag

 TODO: Create a FishNet2 Django Application that contains nothing but
 abstract base classes for these models that other project types inherit from.


 A. Cottrill
=============================================================

"""

from django.db import models
from django.template.defaultfilters import slugify


class FN125_Tag(models.Model):
    """a table for the tag(s) assoicated with a fish."""

    fish = models.ForeignKey("FN125", related_name="fishtags", on_delete=models.CASCADE)
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
