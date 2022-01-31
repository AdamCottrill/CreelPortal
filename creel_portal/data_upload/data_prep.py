"""
=============================================================
~/fn_portal/data_upload/data_prep.py
Created: Aug-12-2021 16:03
DESCRIPTION:

  Functions that take the raw data from our sql
  queries and perform final transformations before creating
  Django objects.

  TODO: consider replacing these fucntions with Pydantic Models.


A. Cottrill
=============================================================
"""

from pydantic.error_wrappers import ValidationError

from .schemas import (
    FN011,
    FN022,
    FN023,
    FN024,
    FN025,
    FN026,
    FN028,
    FN111,
    FN112,
    FN121,
    FN123,
    FN125,
    FN125Tags,
    FN125Lamprey,
    FN126,
    FN127,
)

from .fetch_utils import strip_date


def fn011(data, lake_cache, user_cache, FOF2LAKE):
    valid = []
    errors = []

    for item in data:
        prj_ldr = item.pop("prj_ldr", "")
        prj_cd = item.get("prj_cd")
        lake_abbrev = FOF2LAKE[prj_cd[:3]]
        item["lake_id"] = lake_cache.get(lake_abbrev)
        item["slug"] = prj_cd.lower()
        item["prj_ldr_id"] = user_cache.get(prj_ldr.upper())
        try:
            tmp = FN011(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn022(data, fn011_cache):
    """pop off prj_cd and replace it with creel_id."""

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        ssn = item.get("ssn")
        parent_key = f"{prj_cd}".lower()
        item["creel_id"] = fn011_cache.get(parent_key)
        slug = f"{prj_cd}-{ssn}"
        item["slug"] = slug.lower()
        try:
            tmp = FN022(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn023(data, fn022_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        ssn = item.pop("ssn")
        parent_key = f"{prj_cd}-{ssn}".lower()
        item["season_id"] = fn022_cache.get(parent_key)
        dtp = item.get("dtp")
        slug = f"{prj_cd}-{ssn}-{dtp}"
        item["slug"] = slug.lower()
        try:
            tmp = FN023(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn024(data, fn023_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        ssn = item.pop("ssn")
        dtp = item.pop("dtp")
        parent_key = f"{prj_cd}-{ssn}-{dtp}".lower()
        item["daytype_id"] = fn023_cache.get(parent_key)
        prd = item.get("prd")
        slug = f"{prj_cd}-{ssn}-{dtp}-{prd}"
        item["slug"] = slug.lower()
        try:
            tmp = FN024(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn025(data, fn022_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        ssn = item.pop("ssn")
        parent_key = f"{prj_cd}-{ssn}".lower()
        item["season_id"] = fn022_cache.get(parent_key)
        date = item.get("date")
        slug = f"{prj_cd}-{ssn}-{date}"
        item["slug"] = slug.lower()
        try:
            tmp = FN025(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn026(data, fn011_cache):
    """pop off prj_cd and replace it with creel_id."""

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        space = item.get("space")
        parent_key = f"{prj_cd}".lower()
        item["creel_id"] = fn011_cache.get(parent_key)
        slug = f"{prj_cd}-{space}"
        item["slug"] = slug.lower()
        try:
            tmp = FN026(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn028(data, fn011_cache):

    valid = []
    errors = []

    for item in data:

        prj_cd = item.pop("prj_cd")
        mode = item["mode"]
        parent_key = f"{prj_cd}".lower()
        item["creel_id"] = fn011_cache.get(parent_key)
        slug = f"{prj_cd}-{mode}"
        item["slug"] = slug.lower()
        try:
            tmp = FN028(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn111(
    data, fn011_cache, fn022_cache, fn023_cache, fn024_cache, fn026_cache, fn028_cache
):

    valid = []
    errors = []

    for item in data:

        prj_cd = item.pop("prj_cd")
        stratum = item.pop("stratum")
        # season = item.pop("season")
        # daytype = item.pop("daytype")
        # period = item.pop("
        season = stratum[:2]
        daytype = stratum[3]
        period = stratum[4]

        mode = item.get("mode")
        space = item.get("space")

        parent_key = f"{prj_cd}".lower()
        item["creel_id"] = fn011_cache.get(parent_key)

        season_key = f"{prj_cd}-{season}".lower()
        item["season_id"] = fn022_cache.get(season_key)

        daytype_key = f"{prj_cd}-{season}-{daytype}".lower()
        item["daytype_id"] = fn023_cache.get(daytype_key)

        period_key = f"{prj_cd}-{season}-{period}".lower()
        item["period_id"] = fn023_cache.get(period_key)

        space_key = f"{prj_cd}-{space}".lower()
        item["area_id"] = fn026_cache.get(space_key)

        mode_key = f"{prj_cd}-{mode}".lower()
        item["mode_id"] = fn028_cache.get(mode_key)

        sama = item["sama"]
        slug = f"{prj_cd}-{sama}"
        item["slug"] = slug.lower()
        try:
            tmp = FN111(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn112(data, fn111_cache):

    valid = []
    errors = []

    for item in data:

        prj_cd = item.pop("prj_cd")
        sama = item.pop("sama")
        parent_key = f"{prj_cd}-{sama}".lower()
        item["sama_id"] = fn111_cache.get(parent_key)
        atytm0 = item.get("atytm0")
        slug = f"{prj_cd}-{sama}-{strip_date(atytm0)}"
        item["slug"] = slug.lower()
        try:
            tmp = FN112(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn121(data, fn111_cache):

    valid = []
    errors = []

    counter = 1
    old_sama = ""

    for item in data:
        prj_cd = item.pop("prj_cd")
        sama = item.pop("sama")
        parent_key = f"{prj_cd}-{sama}".lower()
        sam = item["sam"]
        slug = f"{prj_cd}-{sam}".lower()
        item["slug"] = slug
        item["sama_id"] = fn111_cache.get(parent_key)

        # if itvseq is null or '' use our counter
        itvseq = item.get("itvseq")
        if itvseq is None or itvseq == "":
            item["itvseq"] = counter
        counter = 1 if old_sama != sama else counter + 1
        old_sama = sama

        try:
            tmp = FN121(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn123(data, fn121_cache, species_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        spc = item.pop("spc")
        grp = item.get("grp")
        parent_key = f"{prj_cd}-{sam}".lower()
        slug = f"{prj_cd}-{sam}-001-{spc}-{grp}".lower()
        item["interview_id"] = fn121_cache.get(parent_key)
        item["species_id"] = species_cache.get(spc)
        item["slug"] = slug

        try:
            tmp = FN123(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn125(data, fn123_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.get("fish")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        item["catch_id"] = fn123_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN125(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn125tags(data, fn125_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.pop("fish")
        fish_tag_id = item.get("fish_tag_id")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}-{fish_tag_id}".lower()
        item["fish_id"] = fn125_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN125Tags(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn125lamprey(data, fn125_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.pop("fish")
        lamid = item.get("lamid")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}-{lamid}".lower()
        item["fish_id"] = fn125_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN125Lamprey(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn126(data, fn125_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.pop("fish")
        food = item.get("food")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}-{food}".lower()
        item["fish_id"] = fn125_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN126(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn127(data, fn125_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.pop("fish")
        ageid = item.get("ageid")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}-{ageid}".lower()
        item["fish_id"] = fn125_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN127(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}
