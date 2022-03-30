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


class FN026(models.Model):
    """Class to represent the spatial strat used in a creel."""

    creel = models.ForeignKey(
        "FN011", related_name="spatial_strata", on_delete=models.CASCADE
    )
    space = models.CharField(
        max_length=2, blank=False, help_text="Space Code", db_index=True
    )
    space_des = models.CharField(
        max_length=100, blank=False, help_text="Space Description"
    )
    space_siz = models.IntegerField(blank=True, null=True)
    area_cnt = models.IntegerField(blank=True, null=True)
    area_lst = models.CharField(
        max_length=20, help_text="Area List", blank=True, null=True
    )
    area_wt = models.FloatField(blank=True, null=True)

    label = models.CharField(max_length=110, blank=False, help_text="Space Label")

    slug = models.SlugField(blank=True, unique=True, editable=False)

    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN026 - Spatial Strata"
        verbose_name_plural = "FN026 - Spatial Strata"
        ordering = ["space"]
        unique_together = ["creel", "space"]

    def __str__(self):
        """return the object type, the space name, the space code, and
        project code of the creel this record is assoicated with.

        """

        repr = "<Space: {} ({}) [{}]>"
        return repr.format(self.space_des, self.space, self.creel.prj_cd)

    def save(self, *args, **kwargs):
        """
        Create a space label as a combination of the space description
        and space code.
        """

        raw_slug = "-".join([self.creel.prj_cd, self.space])

        self.slug = slugify(raw_slug)

        if self.space_des:
            self.label = "{}-{}".format(self.space, self.space_des.title())
        else:
            self.label = "{}".format(self.space)
        super(FN026, self).save(*args, **kwargs)


#    @property
#    def label(self):
#        """a string that will be used in serialized respoonse for this strata.
#        If both the space, and space_des are available, return them, otherwise,
#        return just the snn code.
#
#        Arguments:
#        - `self`:
#
#        """
#        if self.space_des:
#            label = '{}-{}'.format(self.space, self.space_des.title())
#        else:
#            label = '{}'.format(self.space)
#        return label
#
#
#    @property
#    def popupContent(self):
#        if self.space_des:
#            return "<p>Space: {} ({})</p>".format(self.space_des.title(),
#                                                  self.space)
#        else:
#            return "<p>Space: {}</p>".format(self.space)
#
