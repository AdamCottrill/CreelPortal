"""=============================================================
~/creel_portal/creel_portal/models/CreelTables.py
 Created: 30 Mar 2020 08:49:17

 DESCRIPTION:

  This file contains all of the design tables from a
  fishnet-II/Creesys project that are specific to creels.

+ FN022
+ FN023
+ FN024
+ FN025
+ FN026
+ FN028
+ FN111
+ FN112
+ Strata


 A. Cottrill
=============================================================

"""
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class FN028(models.Model):
    """Class to represent the fishing modes used in a creel."""

    UNIT_CHOICES = ((1, "person"), (2, "party"))

    CHKFLAG_CHOICES = ((0, "No"), (1, "Yes"))

    creel = models.ForeignKey("FN011", related_name="modes", on_delete=models.CASCADE)
    mode = models.CharField(
        help_text="Mode Code", max_length=2, blank=False, db_index=True
    )
    mode_des = models.CharField(
        help_text="Fishing Mode Description", max_length=100, blank=False
    )
    atyunit = models.IntegerField(
        help_text="Activity Unit", default=1, choices=UNIT_CHOICES
    )
    itvunit = models.IntegerField(
        help_text="Interview Unit", default=1, choices=UNIT_CHOICES
    )
    chkflag = models.IntegerField(
        help_text="Check Flag", default=0, choices=CHKFLAG_CHOICES
    )

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN028 - Fishing Mode"
        ordering = ["mode"]
        unique_together = ["creel", "mode"]

    def __str__(self):
        """return the object type, the mode name, the mode code, and
        project code of the creel this record is assoicated with.

        """

        repr = "<FishingMode: {} ({}) [{}]>"
        return repr.format(self.mode_des, self.mode, self.creel.prj_cd)

    @property
    def label(self):
        """a string that will be used in serialized respoonse for this strata.
        If both the mode, and mode_des are available, return them, otherwise,
        return just the snn code.

        Arguments:
        - `self`:

        """
        if self.mode_des:
            label = "{}-{}".format(self.mode, self.mode_des.title())
        else:
            label = "{}".format(self.mode)
        return label

    def save(self, *args, **kwargs):
        """Create a unique slug for each fishing mode in this creel."""

        raw_slug = "-".join([self.creel.prj_cd, self.mode])
        self.slug = slugify(raw_slug)
        super(FN028, self).save(*args, **kwargs)
