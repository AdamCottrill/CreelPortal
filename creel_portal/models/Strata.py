"""
=============================================================
~/creel_portal/creel_portal/models/Stata.py
 Created: 30 Mar 2022 10:35:51

 DESCRIPTION:

 This file contains all of the results tables from a fishnet-II project:

 + Strata

 A. Cottrill
=============================================================
"""


from django.db import models


class Strata(models.Model):
    """A table that lies at the intersection of the design and data
    tables.  For new creels, we may want to add a build method that will
    create the stratum table using the cartesian product of all strata in
    the creel plus any defined in FR711
    """

    creel_run = models.ForeignKey(
        "FR711", related_name="strata", on_delete=models.CASCADE
    )

    stratum_label = models.CharField(max_length=11)

    # optional foreign keys:
    season = models.ForeignKey(
        "FN022", related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    daytype = models.ForeignKey(
        "FN023", related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    period = models.ForeignKey(
        "FN024", related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    area = models.ForeignKey(
        "FN026", related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )
    mode = models.ForeignKey(
        "FN028", related_name="strata", blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        app_label = "creel_portal"

        unique_together = ["creel_run", "stratum_label"]
        ordering = ["creel_run__creel__prj_cd", "creel_run__run", "stratum_label"]

    def __str__(self):
        """return the object type, the interview log number (sama), the stratum,
         and project code of the creel this record is assoicated
        with.

        """

        repr = "{}(run:{}): {}"
        return repr.format(
            self.creel_run.creel.prj_cd, self.creel_run.run, self.stratum_label
        )

    @property
    def strat_days(self):
        """Not sure if this should be a property or a field that this updated
        on save().

        Arguments:
        - `self`:
        """
        return self.calc_strat_days()

    @property
    def strat_hours(self):
        """Not sure if this should be a property or a field that this updated
        on save().

        Arguments:
        - `self`:

        """
        return self.calc_strat_hours()

    def calc_strat_days(self):
        """"""
        dtp = self.daytype.dtp
        days = self.season.get_strat_days(dtp)
        return days

    def calc_strat_hours(self):
        """"""
        days = self.calc_strat_days()
        prd_dir = self.period.prd_dur
        return days * prd_dir
