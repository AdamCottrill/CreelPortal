"""=============================================================
 /home/adam/Documents/djcode/creel_portal/utils/helper_fcts.py
 Created: 12 Feb 2017 13:52:24


 DESCRIPTION:

 Helper functions used to prepare and convert data from FN-II sqlite
 database to dango orm model objects.

 A. Cottrill
=============================================================

"""


from common.models import Lake, Species

from creel_portal.models.fishnet2 import FN011, FN121, FN123, FN125
from creel_portal.models.creel import FN022, FN023, FN024, FN026, FN028, FN111
from creel_portal.models.fishnet_results import FR712


def get_Lake_cache():
    """Return a dictionary of django Lake objects keyed off of their
    abbreviations.

    """
    return {x.abbrev: x for x in Lake.objects.all()}


def get_Species_cache():
    """Return a dictionary of django Lake objects keyed off of their
    species code.

    """
    return {x.spc: x for x in Species.objects.all()}


def get_FN011_cache(lake=None):
    """Return a dictionary of django FN011 objects keyed off of their
    project code.  saves calls to the database each time we need a reference to a project.

    """
    if lake:
        qs = {x.prj_cd: x for x in FN011.objects.filter(lake__abbrev=lake)}
    else:
        qs = {x.prj_cd: x for x in FN011.objects.all()}

    return qs


def get_FN022_cache(lake=None):
    """our FN022 cache will be a two level dictionary - first level will be
     the prj_cd, the second witll be season.
    """
    FN022_cache = {}
    if lake:
        seasons = FN022.objects.filter(creel__lake__abbrev=lake).select_related("creel")
    else:
        seasons = FN022.objects.all().select_related("creel")

    for ssn in seasons:
        prj_cd = ssn.creel.prj_cd
        x = FN022_cache.get(prj_cd)
        if x:
            x[ssn.ssn] = ssn
        else:
            x = {ssn.ssn: ssn}
        FN022_cache[prj_cd] = x
    return FN022_cache


def get_FN023_cache(lake=None):
    """
    """
    cache = {}
    if lake:
        items = FN023.objects.filter(season__creel__lake__abbrev=lake).select_related(
            "season", "season__creel"
        )
    else:
        items = FN023.objects.all().select_related("season", "season__creel")

    for item in items:
        key = "{}-{}-{}".format(item.season.creel.prj_cd, item.season.ssn, item.dtp)
        cache[key] = item
    return cache


def get_FN024_cache(lake=None):
    """
    """
    cache = {}

    if lake:
        items = FN024.objects.filter(
            daytype__season__creel__lake__abbrev=lake
        ).select_related("daytype", "daytype__season", "daytype__season__creel")
    else:
        items = FN024.objects.all().select_related(
            "daytype", "daytype__season", "daytype__season__creel"
        )

    for item in items:
        key = "{}-{}-{}-{}".format(
            item.daytype.season.creel.prj_cd,
            item.daytype.season.ssn,
            item.daytype.dtp,
            item.prd,
        )
        cache[key] = item
    return cache


def get_FN026_cache(lake=None):
    """Return a dictionary of dictionaries that reference the spaces
    available for each creel.

    useage:

    fn026 = FN026_cache[prj_cd][space_code]

    """

    FN026_cache = {}
    if lake:
        spaces = FN026.objects.filter(creel__lake__abbrev=lake).select_related("creel")
    else:
        spaces = FN026.objects.all().select_related("creel")

    for space in spaces:
        prj_cd = space.creel.prj_cd
        x = FN026_cache.get(prj_cd)
        if x:
            x[space.space] = space
        else:
            x = {space.space: space}
        FN026_cache[prj_cd] = x
    return FN026_cache


def get_FN026area_cache(lake=None):
    """Return a dictionary of dictionaries that reference the areas
    available for each creel - this is a work around for those creel
    where areas is not the same as space (according to the creesys
    manual, it should be.)

    useage:

    fn026 = FN026_cache[prj_cd][area]

    """

    FN026_cache = {}
    if lake:
        spaces = FN026.objects.filter(creel__lake__abbrev=lake)
    else:
        spaces = FN026.objects.all()

    spaces = spaces.exclude(area_lst__isnull=True).select_related("creel")

    for space in spaces:
        prj_cd = space.creel.prj_cd
        x = FN026_cache.get(prj_cd)
        if x:
            x[space.area_lst] = space
        else:
            x = {space.area_lst: space}
        FN026_cache[prj_cd] = x
    return FN026_cache


def get_FN028_cache(lake=None):
    """Return a dictionary of dictionaries that reference the modes
    available for each creel.

    useage:

    fn028 = FN028_cache[prj_cd][mode_code]

    """

    FN028_cache = {}
    if lake:
        modes = FN028.objects.filter(creel__lake__abbrev=lake).select_related("creel")
    else:
        modes = FN028.objects.all().select_related("creel")

    for mode in modes:
        prj_cd = mode.creel.prj_cd
        x = FN028_cache.get(prj_cd)
        if x:
            x[mode.mode] = mode
        else:
            x = {mode.mode: mode}
        FN028_cache[prj_cd] = x
    return FN028_cache


def get_FN111_cache(lake=None):
    """Return a dictionary of dictionaries that reference the creel logs
    available for each creel.

    useage:

    fn111 = FN111_cache[prj_cd][sama]
    """
    cache = {}
    if lake:
        samas = FN111.objects.filter(creel__lake__abbrev=lake).select_related("creel")
    else:
        samas = FN111.objects.all().select_related("creel")

    for sama in samas:
        prj_cd = sama.creel.prj_cd
        x = cache.get(prj_cd)
        if x:
            x[sama.sama] = sama
        else:
            x = {sama.sama: sama}
        cache[prj_cd] = x
    return cache


def get_FN121_cache(lake=None):
    """Return a dictionary of dictionaries that reference the interviews
    available for each creel.

    useage:

    fn121 = FN121_cache[prj_cd][sam]
    """

    cache = {}
    if lake:
        sams = FN121.objects.filter(sama__creel__lake__abbrev=lake).select_related(
            "sama__creel"
        )
    else:
        sams = FN121.objects.all().select_related("sama__creel")

    for sam in sams:
        prj_cd = sam.sama.creel.prj_cd
        x = cache.get(prj_cd)
        if x:
            x[sam.sam] = sam
        else:
            x = {sam.sam: sam}
        cache[prj_cd] = x
    return cache


def get_FN123_cache(lake=None):
    """Return a dictionary of available catch counts that is keyed by a
    string made up of the project code, sam number, species code and
    group

    useage:

    fn123 = FN123_cache["prj_cd-sam-spc-grp"]

    """
    cache = {}
    if lake:
        items = FN123.objects.filter(
            interview__sama__creel__lake__abbrev=lake
        ).select_related("interview", "interview__sama__creel", "species")
    else:
        items = FN123.objects.all().select_related(
            "interview", "interview__sama__creel", "species"
        )
    for item in items:
        key = "{}-{}-{}-{}".format(
            item.interview.sama.creel.prj_cd,
            item.interview.sam,
            item.grp,
            item.species.spc,
        )
        cache[key] = item
    return cache


def get_FN125_cache(lake=None):
    """Return a dictionary of sampled fish that is keyed by a string made
    up of the project code, sam number, species code, group and fish
    number

    useage:

    fn125 = FN125_cache["prj_cd-sam-spc-grp-fish"]

    """
    cache = {}
    if lake:
        items = FN125.objects.filter(
            catch__interview__sama__creel__lake__abbrev=lake
        ).select_related(
            "catch",
            "catch__interview",
            "catch__interview__sama__creel",
            "catch__species",
        )
    else:
        items = FN125.objects.all().select_related(
            "catch",
            "catch__interview",
            "catch__interview__sama__creel",
            "catch__species",
        )
    for item in items:
        key = "{}-{}-{}-{}-{}".format(
            item.catch.interview.sama.creel.prj_cd,
            item.catch.interview.sam,
            item.catch.species.spc,
            item.catch.grp,
            item.fish,
        )
        cache[key] = item
    return cache


def get_FR712_cache(lake=None):
    """Return a dictionary of available of known strata that is keyed by a
    string made up of the project code, run number, strata, and record type
    """
    # FR712 records our unique by: prj_cd, run, rec_tp, strat
    cache = {}
    if lake:
        objects = FR712.objects.filter(
            stratum__creel_run__creel__lake__abbrev=lake
        ).select_related("stratum", "stratum__creel_run", "stratum__creel_run__creel")
    else:
        objects = FR712.objects.all().select_related(
            "stratum", "stratum__creel_run", "stratum__creel_run__creel"
        )
    for item in objects:
        key = "{}-{}-{}-{}".format(
            item.stratum.creel_run.creel.prj_cd,
            item.stratum.creel_run.run,
            item.rec_tp,
            item.stratum.stratum_label,
        )
        cache[key] = item
    return cache


def prj_cd_shouldbe(prj_cd):
    """A little helper function to try and fix the project codes - in some
    tables, the codes look like the prefixes have been changed (as there
    is currently a mis-match between design and data tables.).  Hopefully
    this function will help fix that.

    Arguments:
    - `prj_cd`:

    """

    if prj_cd == "NPW_SC03_NIR":
        return "LSM_SC03_NIP"

    if prj_cd[-3:] in ["BSR", "NIR"]:
        prj_cd = "NPW" + prj_cd[3:]
    else:
        prj_cd = "LSM" + prj_cd[3:]
    return prj_cd


def int_or_none(val, default=None):
    """

    Arguments:
    - `x`:
    """
    if val is None:
        return default
    else:
        try:
            ret = int(val)
        except ValueError:
            ret = default
        return ret


def time_or_none(val):
    """

    Arguments:
    - `x`:
    """
    from datetime import datetime

    if val is None:
        return None
    elif val == "" or val.replace(" ", "") == ":":
        return None
    else:
        try:
            if val == "24:00":
                # use one second before midnight:
                my_time = datetime.strptime("23:59:59", "%H:%M:%S").time()
            else:
                my_time = datetime.strptime(val, "%H:%M").time()
        except ValueError:
            my_time = None
        return my_time


def float_or_none(val, default=None):
    """

    Arguments:
    - `x`:
    """

    if val is None:
        return default
    else:
        try:
            ret = float(val)
        except ValueError:
            ret = default
        return ret


def bool_or_none(val):
    """

    Arguments:
    - `x`:
    """
    from distutils.util import strtobool

    if val is None:
        return None
    elif val == "":
        return None
    else:
        return bool(strtobool(val))


def get_user_attrs(prj_ldr):
    """take a username from a fishnet project and return the first and
    last name, a user address and an ontario email address."""
    attrs = {}

    names = prj_ldr.title().split()
    firstName = names[0]
    if len(names) > 1:
        lastName = names[1]
    else:
        lastName = ""
    attrs["first_name"] = firstName
    attrs["last_name"] = lastName
    attrs["email"] = "{}.{}@ontario.ca".format(firstName.lower(), lastName.lower())
    attrs["username"] = lastName.lower() + firstName.lower()[:2]

    return attrs


def get_combined_strata(creel_run):
    """Given a creel_run, return list of tuples representing rows in the
    strata table for each comibined strata as described in strat_comb.

    Arguments:
    - `creel_run`: a FN011 creel_run object
    - `strat_comb`: a 11 character combination mask of the form '++_++_++_++'

    TODO - implement strata creation when a single strata value is
    requested - this feature is largely obsolete, but associated
    results to exist in creel_run archive.  Currently, these strata and
    results are ignored.

    """

    strat_comb = creel_run.strat_comb

    if strat_comb[:2] == "??":
        season_strata = creel_run.creel.seasons.values_list("ssn", "id")
    else:
        season_strata = [("++", None)]

    if strat_comb[3] == "?":
        # daytype is within season, so we can't have separate daytype
        # strata unless we have separate season strata too
        print("warning - grouping by daytype is not currently implemented")
        daytype_strata = [("+", None)]
    else:
        daytype_strata = [("+", None)]

    if strat_comb[4] == "?":
        # period is within daytype, so we can't have separate periods
        # strata unless we have separate season and daytype strata
        print("warning - grouping by period is not currently implemented")
        period_strata = [("+", None)]
    else:
        period_strata = [("+", None)]

    if strat_comb[6:8] == "??":
        space_strata = creel_run.creel.spatial_strata.values_list("space", "id")
    else:
        space_strata = [("++", None)]

    if strat_comb[9:11] == "??":
        mode_strata = creel_run.creel.modes.values_list("mode", "id")
    else:
        mode_strata = [("++", None)]

    all_strata = []

    for season in season_strata:
        for daytype in daytype_strata:
            for period in period_strata:
                for space in space_strata:
                    for mode in mode_strata:
                        strata = "{}_{}{}_{}_{}".format(
                            season[0], daytype[0], period[0], space[0], mode[0]
                        )
                        all_strata.append(
                            (
                                creel_run.id,
                                strata,
                                season[1],
                                space[1],
                                daytype[1],
                                period[1],
                                mode[1],
                            )
                        )
    return all_strata


def get_strata(creel_run):
    """Given a creel_run, return a list of tuples that represent the rows
    in the Strata table - each row contains the strata label, and foreign
    keys to the corresponding creel_run, season, space, daytype, period and
    fishing mode.

    Arguments:
    - `creel_run`: An FN011 creel_run object.

    """

    all_strata = []
    modes = creel_run.creel.modes.all()
    spots = creel_run.creel.spatial_strata.all()
    seasons = creel_run.creel.seasons.all()

    for season in seasons:
        daytypes = season.daytypes.all()
        for spot in spots:
            for daytype in daytypes:
                periods = daytype.periods.all()
                for period in periods:
                    for mode in modes:
                        strata = "{}_{}{}_{}_{}".format(
                            season.ssn, daytype.dtp, period.prd, spot.space, mode.mode
                        )
                        all_strata.append(
                            (
                                creel_run.id,
                                strata,
                                season.id,
                                spot.id,
                                daytype.id,
                                period.id,
                                mode.id,
                            )
                        )
    return all_strata
