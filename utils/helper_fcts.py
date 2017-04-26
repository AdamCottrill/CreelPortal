'''=============================================================
 /home/adam/Documents/djcode/creel_portal/utils/helper_fcts.py
 Created: 12 Feb 2017 13:52:24


 DESCRIPTION:

 Helper functions used to prepare and convert data from FN-II sqlite
 database to dango orm model objects.

 A. Cottrill
=============================================================

'''



def prj_cd_shouldbe(prj_cd):
    """A little helper function to try and fix the project codes - in some
    tables, the codes look like the prefixes have been changed (as there
    is currently a mis-match between design and data tables.).  Hopefully
    this function will help fix that.

    Arguments:
    - `prj_cd`:

    """

    if prj_cd == 'NPW_SC03_NIR':
        return 'LSM_SC03_NIP'

    if prj_cd[-3:] in ['BSR','NIR']:
        prj_cd = 'NPW' + prj_cd[3:]
    else:
        prj_cd = 'LSM' + prj_cd[3:]
    return prj_cd


def int_or_none(val, default=None):
    """

    Arguments:
    - `x`:
    """
    if val is None:
        if default is not None:
            return default
        else:
            return None
    elif val == "":
        if default is not None:
            return default
        else:
            return None
    else:
        return int(val)


def time_or_none(val):
    """

    Arguments:
    - `x`:
    """
    from datetime import datetime
    if val is None:
        return None
    elif val=="" or val.replace(' ','')==':':
        return None
    else:
        return datetime.strptime(val,'%H:%M')


def float_or_none(val):
    """

    Arguments:
    - `x`:
    """

    if val is None:
        return None
    elif val == "":
        return None
    else:
        return float(val)


def bool_or_none(val):
    """

    Arguments:
    - `x`:
    """
    from distutils.util import strtobool

    if val is None:
        return None
    elif val == '':
        return None
    else:
        return bool(strtobool(val))


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
        season_strata =  creel_run.creel.seasons.values_list('ssn', 'id')
    else:
        season_strata = [('++',None),]

    if strat_comb[3] == "?":
        #daytype is within season, so we can't have separate daytype
        #strata unless we have separate season strata too
        print("warning - grouping by daytype is not currently implemented")
        daytype_strata = [('+', None),]
    else:
        daytype_strata = [('+', None),]

    if strat_comb[4] == "?":
        #period is within daytype, so we can't have separate periods
        #strata unless we have separate season and daytype strata
        print("warning - grouping by period is not currently implemented")
        period_strata = [('+', None),]
    else:
        period_strata = [('+', None),]

    if strat_comb[6:8] == "??":
        space_strata =  creel_run.creel.spatial_strata.\
                        values_list('space', 'id')
    else:
        space_strata = [('++', None),]

    if strat_comb[9:11] == "??":
        mode_strata =  creel_run.creel.modes.values_list('mode', 'id')
    else:
        mode_strata = [('++', None),]

    all_strata = []

    for season in season_strata:
        for daytype in daytype_strata:
            for period in period_strata:
                for space in space_strata:
                    for mode in mode_strata:
                        strata = '{}_{}{}_{}_{}'.format(
                            season[0],  daytype[0], period[0],
                            space[0], mode[0])
                        all_strata.append((creel_run.id, strata, season[1],
                                           space[1], daytype[1], period[1],
                                           mode[1]))
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
                        strata = '{}_{}{}_{}_{}'.format(
                            season.ssn, daytype.dtp, period.prd,
                            spot.space, mode.mode)
                        all_strata.append((creel_run.id, strata, season.id,
                                           spot.id, daytype.id, period.id,
                                           mode.id))
    return all_strata
