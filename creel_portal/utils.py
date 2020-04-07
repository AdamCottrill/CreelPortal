"""
=============================================================
~/creel_portal/creel_portal/utils.py
 Created: 06 Apr 2020 17:18:23

 DESCRIPTION:



 A. Cottrill
=============================================================
"""

import json

from django.db.models import Sum, F

from common.models import Species
from .models.fishnet_results import FR713, FR714


def get_aggregate_effort_estimates(creel, run=None):
    """Given a creel object and optionally a creel run, return the catch
    estimate objects from the top-most, aggregate strata.  If the
    strat_comb was ++_++_++_++, only a single record per species and
    sek will be returned, but it the mast included one or more ?, then
    one record will be returned for each level in the strata
    correspondind to the ?.

    Arguments:
    - `creel`:
    - `run`:
    """

    if run is None:
        if creel.final_run is None:
            return None
        else:
            run = creel.final_run.run

    my_run = creel.creel_run.get(run=run)

    qs = FR713.objects.filter(
        fr712__rec_tp=3, fr712__stratum__creel_run=my_run
    ).select_related("fr712__stratum")

    return qs

    # mask_re = my_run.strat_comb.replace("?", "\w").replace("+", "\+")

    # my_strata = my_run.strata.filter(stratum_label__regex=mask_re).all()
    # estimates = []
    # for x in my_strata:
    #     strata = x.stratum_label
    #     tmp = FR713.objects.filter(fr712__stratum=x)
    #     estimates.append({"strata": strata, "estimates": tmp})

    # return estimates


def get_aggregate_catch_estimates(creel, run=None):
    """Given a creel object and optionally a creel run, return the catch
    estimate objects from the top-most, aggregate strata.  If the
    strat_comb was ++_++_++_++, only a single record per species and
    sek will be returned, but it the mast included one or more ?, then
    one record will be returned for each level in the strata
    correspondind to the ?.

    Arguments:
    - `creel`:
    - `run`:

    """

    if run is None:
        if creel.final_run is None:
            return None
        else:
            run = creel.final_run.run

    my_run = creel.creel_run.get(run=run)

    qs = FR714.objects.filter(
        fr712__rec_tp=3, fr712__stratum__creel_run=my_run
    ).select_related("fr712__stratum", "species")

    return qs

    # mask_re = my_run.strat_comb.replace("?", "\w").replace("+", "\+")

    # my_strata = my_run.strata.filter(stratum_label__regex=mask_re).all()
    # estimates = []
    # for x in my_strata:
    #     strata = x.stratum_label
    #     tmp = FR714.objects.filter(fr712__stratum=x)
    #     estimates.append({"strata": strata, "estimates": tmp})

    # return estimates


def get_catch_totals(creel, run=None):
    """this function returns a json string containing the observed and
    estimated catch and harvest numbers for this creel.

    If the creel has only one final strata, this query should
    return numbers that are exactly the same as the global strata
    (++_++_++_++), but in cases where strata are maintained
    seperatately (and that strata does not exist), this query
    returns the equivalent values by summing accross all
    individual strata estiamtes.

    TODO: this function should be exposed through an api.

    Arguments:
    - `self`:

    """
    aliases = {"common_name": F("species__spc_nmco")}

    aggregation_metrics = {
        "xcatne": Sum("catne"),
        "xcatne1": Sum("catne1"),
        "xcatno_s": Sum("catno_s"),
        "xcatno1_s": Sum("catno1_s"),
        "xhvsno_s": Sum("hvsno_s"),
        "xhvsno1_s": Sum("hvsno1_s"),
        "xhvsne": Sum("hvsne"),
        "xhvsne1": Sum("hvsne1"),
    }

    if run is None:
        if creel.final_run is None:
            return None
        else:
            run = creel.final_run.run

    catch_counts = (
        FR714.objects.filter(
            fr712__stratum__creel_run__run=run,
            fr712__stratum__creel_run__creel=creel,
            fr712__rec_tp=2,
        )
        .select_related("species")
        .annotate(**aliases)
        .values("common_name")
        .order_by()
        .annotate(**aggregation_metrics)
    )

    return json.dumps(list(catch_counts))
