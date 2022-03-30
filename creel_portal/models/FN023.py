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


class FN023(models.Model):
    """Class  to represent the daytypes used in each season of creel"""

    DAYTYPE_CHOICES = ((1, "weekday"), (2, "weekend"))

    # creel = models.ForeignKey(FN011)
    season = models.ForeignKey(
        "FN022", related_name="daytypes", on_delete=models.CASCADE
    )
    dtp = models.CharField(
        help_text="Day Type Code",
        max_length=2,
        blank=False,
        db_index=True,
        choices=DAYTYPE_CHOICES,
    )
    dtp_nm = models.CharField(help_text="Day Type Name", max_length=10, blank=False)
    dow_lst = models.CharField(help_text="Day Of Week List", max_length=7, blank=False)

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN023 - Day Type"
        ordering = ["dtp"]
        unique_together = ["season", "dtp"]

    @property
    def creel(self):
        """A shortcut method to directly access the creel object - allows use
        of same permission class on different api endpoints.
        """
        return self.season.creel

    def save(self, *args, **kwargs):
        """ """

        raw_slug = "-".join([self.season.creel.prj_cd, self.season.ssn, self.dtp])

        self.slug = slugify(raw_slug)
        super(FN023, self).save(*args, **kwargs)

    def __str__(self):
        """return the object type, the daytype name, day type code, and the
        code project code of the creel this record is assoicated with.

        """

        repr = "<DayType: {}({}) {}-{}>"
        return repr.format(
            self.dtp_nm, self.dtp, self.season.ssn, self.season.creel.prj_cd
        )

    @property
    def label(self):
        """a string that will be used in serialized respoonse for this strata.
        If both the dtp, and dtp des are available, return them, otherwise,
        return just the snn code.

        Arguments:
        - `self`:

        """
        if self.dtp_nm:
            label = "{}-{}".format(self.dtp, self.dtp_nm.title())
        else:
            label = "{}".format(self.dtp)
        return label
