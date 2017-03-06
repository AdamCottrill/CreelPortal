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
    return None if val == '' else bool(val)
