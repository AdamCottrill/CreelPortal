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

from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from common.models import Lake

from .choices import CONTMETH_CHOICES

User = get_user_model()

# note = move this to main.models too
class FN011(models.Model):
    """Class to hold a record for each project"""

    lake = models.ForeignKey(
        Lake, default=1, related_name="creels", on_delete=models.CASCADE
    )

    prj_ldr = models.ForeignKey(
        User,
        help_text="Project Lead",
        related_name="creels",
        blank=False,
        on_delete=models.CASCADE,
    )
    field_crew = models.ManyToManyField(User, related_name="creel_crew")

    prj_date0 = models.DateField(help_text="Start Date", blank=False)
    prj_date1 = models.DateField(help_text="End Date", blank=False)
    prj_cd = models.CharField(
        help_text="Project Code", max_length=12, unique=True, blank=False
    )
    year = models.CharField(
        help_text="Year", max_length=4, blank=True, editable=False, db_index=True
    )
    prj_nm = models.CharField(help_text="Project Name", max_length=60, blank=False)

    comment0 = models.TextField(
        blank=True, null=True, help_text="General Project Description."
    )
    slug = models.SlugField(blank=True, unique=True, editable=False)

    # contmeth is repeated in FR711 table - will have to figure out how
    # to keep them in sync.
    contmeth = models.CharField(
        help_text="Creel Type",
        max_length=2,
        db_index=True,
        choices=CONTMETH_CHOICES,
        default="A2",
    )

    class Meta:
        app_label = "creel_portal"
        verbose_name = "FN011 - Creel"
        ordering = ["-prj_date1"]

    def get_absolute_url(self):
        """return the url for the project"""
        url = reverse("creel_portal:creel_detail", kwargs={"slug": self.slug})
        return url
        # return reverse("creel_detail", {"slug": self.slug})

    def __str__(self):
        """return the creel name and project code as its string
        representation"""
        return "<Creel: {} ({})>".format(self.prj_nm, self.prj_cd)

    def save(self, *args, **kwargs):
        """
        from:http://stackoverflow.com/questions/7971689/
             generate-slug-field-in-existing-table
        Slugify name if it doesn't exist. IMPORTANT: doesn't check to see
        if slug is a dupicate!
        """

        self.slug = slugify(self.prj_cd)
        self.year = self.prj_date0.year
        super(FN011, self).save(*args, **kwargs)

    def get_global_strata(self):
        """This function will return the global strata of the the last run of
        this creel. If the mask is "++_++_++_++", a single object will
        be returned correspondng to a single record in the FR712
        table. if the mask contains any ? - one record will be
        returned for each level in the corresponding stratum.
        """

        my_run = self.creel_run.order_by("-run").first()

        mask_re = my_run.strat_comb.replace("?", "\w").replace("+", "\+")

        my_strata = my_run.strata.filter(stratum_label__regex=mask_re).all()

        return my_strata

    def get_global_effort(self):
        """Return the final effort estimates for this creel at the highest
        level of aggregation.  If strat_comb indicates that all strata
        are to be collapsed, then the result is one element list
        containing the estimates.  If strat_comb indicates that one or
        more strata are not to be combined, this function returns a
        list with one element corresponding to each strata level.

        By default, the last run a creel is always returned.  This
        assumes that each run is an improvement on previous runs.
        This could be re-considered if necessary."""

        # get the globals for a creel:
        # return the estimates from the last run
        # TODO - we need to get multiple objects if the comb_strat contains
        # any '??'
        # effort = self.creel_run.order_by('-run').first().\
        #         strata.filter(stratum_label='++_++_++_++').\
        #         first().effort_estimates.get()

        my_run = self.creel_run.order_by("-run").first()

        mask_re = my_run.strat_comb.replace("?", "\w").replace("+", "\+")

        my_strata = my_run.strata.filter(stratum_label__regex=mask_re).all()

        estimates = []
        # for x in my_strata:
        #    # strata = [x.season, x.daytype, x.period, x.area, x.mode]
        #    strata = x.stratum_label
        #    # tmp = x.effort_estimates.get()
        #    estimates.append({"strata": strata, "estimates": tmp})

        return estimates

    @property
    def final_run(self):
        """Return the final creel run - assumes that the run with the highest
        number is preferred. This may not be case.

        Arguments:
        - `self`:

        """
        return self.creel_run.order_by("-run").first()

    # def get_global_catch(self):
    #     """Return the final catch estimates for this creel at the highest
    #     level of aggregation.  If strat_comb indicates that all strata
    #     are to be collapsed, then the result is one element list
    #     containing the estimates.  If strat_comb indicates that one or
    #     more strata are not to be combined, this function returns a
    #     list with one element corresponding to each strata level.

    #     By default, the last run a creel is always returned.  This
    #     assumes that each run is an improvement on previous runs.
    #     This could be re-considered if necessary.

    #     """

    #     # catch_est = self.creel_run.order_by('-run').first().\
    #     #            strata.filter(stratum_label='++_++_++_++').\
    #     #            first().catch_estimates.all()
    #     # return catch_est

    #     my_run = self.creel_run.order_by("-run").first()

    #     mask_re = my_run.strat_comb.replace("?", "\w").replace("+", "\+")
    #     # my_strata = my_run.strata.filter(stratum_label__regex=mask_re).all()
    #     # estimates = []
    #     # for x in my_strata:
    #     #     # strata = [x.season, x.daytype, x.period, x.area, x.mode]
    #     #     strata = x.stratum_label
    #     #     #tmp = FR714.objects.filter(fr712__stratum=x)
    #     #     tmp = x.catch_estimates.all()
    #     #     estimates.append({"strata": strata, "estimates": tmp})

    #     return my_run.strata.filter(stratum_label__regex=mask_re).all()

    # def get_catch_totals(self):
    #     """this function returns a json string containing the observed and
    #     estimated catch and harvest numbers for this creel.

    #     If the creel has only one final strata, this query should
    #     return numbers that are exactly the same as the global strata
    #     (++_++_++_++), but in cases where strata are maintained
    #     seperatately (and that strata does not exist), this query
    #     returns the equivalent values by summing accross all
    #     individual strata estiamtes.

    #     TODO: this function should be exposed through an api.

    #     Arguments:
    #     - `self`:

    #     """
    #     # aliases = {"common_name": F("species__common_name")}

    #     # aggregation_metrics = {
    #     #     "xcatne": Sum("catne"),
    #     #     "xcatne1": Sum("catne1"),
    #     #     "xcatno_s": Sum("catno_s"),
    #     #     "xcatno1_s": Sum("catno1_s"),
    #     #     "xhvsno_s": Sum("hvsno_s"),
    #     #     "xhvsno1_s": Sum("hvsno1_s"),
    #     #     "xhvsne": Sum("hvsne"),
    #     #     "xhvsne1": Sum("hvsne1"),
    #     # }

    #     # catch_counts = (
    #     #     FR714.objects.filter(stratum__creel_run=self.final_run, rec_tp=2)
    #     #     .annotate(**aliases)
    #     #     .values("common_name")
    #     #     .order_by()
    #     #     .annotate(**aggregation_metrics)
    #     # )

    #     # return json.dumps(list(catch_counts))

    #     return None
