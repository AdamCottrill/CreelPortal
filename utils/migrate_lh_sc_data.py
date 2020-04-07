"""
=============================================================
 /home/adam/Documents/djcode/creel_portal/utils/migrate_ls_sc_data.py
 Created: 11 Feb 2017 15:40:28


 DESCRIPTION:


 A. Cottrill
=============================================================
"""


import django
import sqlite3
import os

from datetime import datetime

os.chdir("./..")

import django_settings

django.setup()


from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify


from common.models import Lake, Species

from creel_portal.models.fishnet2 import (
    FN011,
    FN121,
    FN123,
    FN125,
    FN125_Lamprey,
    FN125_Tag,
)
from creel_portal.models.creel import (
    FN022,
    FN023,
    FN024,
    FN025,
    FN026,
    FN028,
    FN111,
    FN112,
)

from creel_portal.models.fishnet_results import (
    Strata,
    FR711,
    FR712,
    FR713,
    FR714,
    FR715,
)


from utils.helper_fcts import (
    int_or_none,
    get_strata,
    get_combined_strata,
    bool_or_none,
    float_or_none,
    time_or_none,
    get_user_attrs,
    get_Species_cache,
    get_FN011_cache,
    get_FN022_cache,
    get_FN023_cache,
    get_FN024_cache,
    get_FN026_cache,
    get_FN028_cache,
    get_FN111_cache,
    get_FN121_cache,
    get_FN123_cache,
    get_FN125_cache,
    get_FR712_cache,
)

species_cache = get_Species_cache()
FN011_cache = get_FN011_cache()
FN022_cache = get_FN022_cache()
FN023_cache = get_FN023_cache()
FN024_cache = get_FN024_cache()
FN026_cache = get_FN026_cache()
FN028_cache = get_FN028_cache()
FN111_cache = get_FN111_cache()
FN122_cache = get_FN121_cache()
FN123_cache = get_FN123_cache()
FN125_cache = get_FN125_cache()
FR712_cache = get_FR712_cache()


User = get_user_model()


# SRC_DB = '/home/adam/Documents/work/Superior/SC_master.db'
# SRC_DB = '/home/adam/Documents/work/Superior/lhmu_sc_warehouse.db'
SRC_DB = "C:/Users/COTTRILLAD/1work/ScrapBook/lhmu_sc_warehouse_clean.db"


conn = sqlite3.connect(SRC_DB)
cursor = conn.cursor()

# get our users

sql = "select distinct prj_ldr from FN011;"

cursor.execute(sql)
rs = cursor.fetchall()


# loop over out users - create a dictionary keyed on the values returned as project leads:

users = {}

for rec in rs:
    prj_ldr = rec[0] if rec[0] != "" else "SUPER BIO"
    users[rec[0]] = get_user_attrs(prj_ldr)


# there are a couple of duplicate entries we need to address:
users["DAVID REID"] = users["DAVE REID"]
users["DANACOUTURE"] = users["DANA COUTURE"]
users["ARUNAS LISKAUSKAS/LLOYD MOHR"] = users["ARUNAS LISKAUSKAS"]

# now loop over all of our users and get or create each user.  When we
# get our user back, add it as the value to our user cache so we can
# add the relationship when we create the FN011 record.

user_cache = {}
for key, values in users.items():
    user, created, = User.objects.get_or_create(**values)
    user.save()
    user_cache[key.upper()] = user


# lake = Lake(lake_name='Huron', abbrev='HU')
# lake.save()

lake = Lake.objects.get(abbrev="HU")
print("Working on Lake " + str(lake))
# ==================================
#    FN011  - Project Details

sql = """select PRJ_CD, ARU, COMMENT0, FOF_LOC, FOF_NM, PRJ_DATE0,
         PRJ_DATE1, PRJ_HIS, PRJ_LDR, PRJ_NM, PRJ_SIZE, PRJ_VER,
         V0, WBY WBY_NM from fn011;"""

cursor.execute(sql)
rs = cursor.fetchall()

col_names = [x[0].lower() for x in cursor.description]
# projects must be created individually as they have save()
# method that generates a slug
for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_ldr = x.pop("prj_ldr")
    x["prj_ldr"] = user_cache[prj_ldr.upper()]

    x["lake"] = lake
    yr = datetime.strptime(x["prj_cd"][6:8], "%y").year
    x["year"] = yr
    prj_date0 = datetime.strptime(x["prj_date0"], "%Y-%m-%d")
    prj_date1 = datetime.strptime(x["prj_date1"], "%Y-%m-%d")
    x["prj_date0"] = prj_date0.replace(year=yr)
    x["prj_date1"] = prj_date1.replace(year=yr)
    x["prj_cd"] = x["prj_cd"]
    creel = FN011(**x)
    creel.save()
print("Done adding FN011 records.")

FN011_cache = get_FN011_cache()


# ==================================
#  FN022 - Temporal/Seasonal Strata:

sql = """SELECT PRJ_CD, SSN, SSN_DATE0, SSN_DATE1, SSN_DES
         from fn022;"""
cursor.execute(sql)
rs = cursor.fetchall()
objects = []
col_names = [x[0].lower() for x in cursor.description]
for record in rs:
    x = {k: v for k, v in zip(col_names, record)}

    yr = datetime.strptime(x["prj_cd"][6:8], "%y").year
    ssn_date0 = datetime.strptime(x["ssn_date0"], "%Y-%m-%d")
    ssn_date1 = datetime.strptime(x["ssn_date1"], "%Y-%m-%d")
    x["ssn_date0"] = ssn_date0.replace(year=yr)
    x["ssn_date1"] = ssn_date1.replace(year=yr)
    prj_cd = x.pop("prj_cd")
    x["creel"] = FN011.objects.get(prj_cd=prj_cd)

    slug = "-".join([prj_cd, x.get("ssn")])
    x["slug"] = slugify(slug)

    item = FN022(**x)
    # item.save()
    objects.append(item)

FN022.objects.bulk_create(objects)
print("Done adding FN022 records.")


# our FN022 cache will be a two level dictionary - first level will be
# the prj_cd, the second witll be season.
FN022_cache = get_FN022_cache()


# ==================================
#    FN023 -  Day Types Strata

sql = """SELECT PRJ_CD, SSN, DOW_LST, DTP, DTP_NM from FN023;"""
cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    ssn = x.pop("ssn")
    # season = FN022.objects.filter(creel__prj_cd=prj_cd, ssn=ssn).get()
    season = FN022_cache[prj_cd][ssn]
    x["season"] = season

    slug = "-".join([prj_cd, ssn, x.get("dtp")])
    x["slug"] = slugify(slug)

    item = FN023(**x)
    # item.save()
    objects.append(item)
FN023.objects.bulk_create(objects)


print("Done adding FN023 records.")

FN023_cache = get_FN023_cache()


# ==================================
#    FN024 - Periods

sql = """SELECT PRJ_CD, SSN, DTP, PRD, PRDTM0, PRDTM1, PRD_DUR from FN024;"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    ssn = x.pop("ssn")
    dtp = x.pop("dtp")
    key = "{}-{}-{}".format(prj_cd, ssn, dtp)
    daytype = FN023_cache[key]

    x["daytype"] = daytype
    x["prdtm0"] = datetime.strptime(x["prdtm0"], "%H:%M")
    x["prdtm1"] = datetime.strptime(x["prdtm1"], "%H:%M")

    slug = "-".join([prj_cd, ssn, dtp, x.get("prd")])
    x["slug"] = slugify(slug)

    item = FN024(**x)
    # item.save()
    objects.append(item)
FN024.objects.bulk_create(objects)
print("Done adding FN024 records.")

FN024_cache = get_FN024_cache()


# ==================================
#     FN025 - Exception Dates

sql = """SELECT PRJ_CD, [DATE], DTP1 from FN025;"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    yr = datetime.strptime(prj_cd[6:8], "%y").year
    my_date = datetime.strptime(x["date"], "%Y-%m-%d")
    my_date = my_date.replace(year=yr)
    season = (
        FN022.objects.filter(ssn_date0__lte=my_date)
        .filter(ssn_date1__gte=my_date)
        .filter(creel__prj_cd=prj_cd)
        .get()
    )
    x["season"] = season
    x["date"] = my_date
    item = FN025(**x)
    # item.save()
    objects.append(item)
FN025.objects.bulk_create(objects)
print("Done adding FN025 records.")


# ==================================
#  FN026  - Spatial Strata

sql = """SELECT prj_cd, space, space_des, space_siz, area_cnt,
         area_lst, area_wt from FN026;"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    x["creel"] = FN011.objects.get(prj_cd=prj_cd)
    x["space_siz"] = int_or_none(x["space_siz"])
    x["area_cnt"] = int_or_none(x["area_cnt"])
    x["area_wt"] = int_or_none(x["area_wt"])

    slug = "-".join([prj_cd, x.get("space")])
    x["slug"] = slugify(slug)

    item = FN026(**x)
    # item.save()
    objects.append(item)
FN026.objects.bulk_create(objects)
print("Done adding FN026 records.")

FN026_cache = get_FN026_cache()

# ==================================
#    FN028  - Fishing Modes

sql = """SELECT PRJ_CD, ATYUNIT, CHKFLAG, ITVUNIT, MODE,
         MODE_DES from FN028 where V0 <> '.++';"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    x["creel"] = FN011.objects.get(prj_cd=prj_cd)
    x["atyunit"] = int_or_none(x["atyunit"])
    x["itvunit"] = int_or_none(x["itvunit"])
    x["chkflag"] = int_or_none(x["chkflag"])

    slug = "-".join([prj_cd, x.get("mode")])
    x["slug"] = slugify(slug)

    item = FN028(**x)
    # item.save()
    objects.append(item)
FN028.objects.bulk_create(objects)
print("Done adding FN028 records.")

FN028_cache = get_FN028_cache()

# ==================================
#          FR711

# the FR711 table holds the settings for the analysis -
# the type of creel, the activity unit and the strata mask.

sql = """select prj_cd, run, contmeth, do_cif, fr71_est,
         fr71_unit, atycrit, cifopt, strat_comb, save_daily,
         mask_c from fr711 order by prj_cd, run;
"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    creel = FN011_cache.get(prj_cd)

    if creel is None:
        msg = "{} not found.".format(prj_cd)
        continue
    else:
        x["creel"] = creel
    item = FR711(**x)
    item.save()
    # objects.append(item)
# FR711.objects.bulk_create(objects)
print("Done adding FR711 records.")


# ==================================
#          STRATA

# now we need to build the strata for each project from the design tables and the
# strat_mask in the FR711 table:

fr711s = FR711.objects.all()

all_strata = []
for creel_run in fr711s:
    combined_strata = get_combined_strata(creel_run)
    all_strata.extend(combined_strata)
    other_strata = get_strata(creel_run)
    all_strata.extend(other_strata)

objects = []
col_names = [
    "creel_run_id",
    "stratum_label",
    "season_id",
    "area_id",
    "daytype_id",
    "period_id",
    "mode_id",
]

for x in all_strata:
    x = {k: v for k, v in zip(col_names, x)}
    item = Strata(**x)
    objects.append(item)
Strata.objects.bulk_create(objects)
print("Done adding Strata records.")


# ==================================
#    FN111  - Interview Logs

sql = """SELECT prj_cd, sama, [date], samtm0, area, mode,
         weather, comment1 from FN111"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:

    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    yr = datetime.strptime(prj_cd[6:8], "%y").year
    my_date = datetime.strptime(x["date"], "%Y-%m-%d")
    my_date = my_date.replace(year=yr)
    my_time = datetime.strptime(x["samtm0"], "%H:%M").time()

    x["date"] = my_date
    x["samtm0"] = my_time

    creel = FN011_cache[prj_cd]
    x["creel"] = creel

    season = (
        FN022.objects.filter(creel__prj_cd=prj_cd)
        .filter(ssn_date0__lte=my_date)
        .filter(ssn_date1__gte=my_date)
        .get()
    )
    x["season"] = season

    my_dow = int(datetime.strftime(my_date, "%w")) + 1
    daytype = (
        FN023.objects.filter(season=season).filter(dow_lst__contains=str(my_dow)).get()
    )
    x["daytype"] = daytype

    period = (
        FN024.objects.filter(daytype=daytype)
        .filter(prdtm0__lte=my_time, prdtm1__gt=my_time)
        .get()
    )
    x["period"] = period

    exception_date = FN025.objects.filter(season=season, date=my_date).first()
    if exception_date:
        x["daycode"] = exception_date.dtp1
    else:
        x["daycode"] = daytype.dtp

    area_code = x["area"]
    # area = FN026.objects.get(creel=creel, space=area_code)
    # x['area'] = area

    x["area"] = FN026_cache[prj_cd][area_code]

    mode_code = x["mode"]
    # mode = FN028.objects.get(creel=creel, mode=mode_code)
    # x['mode'] = mode
    x["mode"] = FN028_cache[prj_cd][mode_code]

    x["weather"] = int_or_none(x["weather"])

    slug = "-".join([prj_cd, x.get("sama")])
    x["slug"] = slugify(slug)

    item = FN111(**x)
    # item.save()
    objects.append(item)
FN111.objects.bulk_create(objects)
print("Done adding FN111 records.")


FN111_cache = get_FN111_cache()


# ==================================
#    FN112  - ActivityCounts

sql = """select prj_cd, sama, atytm0, atytm1, atycnt, chkcnt,
         itvcnt from fn112 order by prj_cd, sama"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    _sama = x.pop("sama")
    # sama = FN111.objects.filter(creel__prj_cd=prj_cd, sama=sama).get()
    sama = FN111_cache[prj_cd][str(_sama)]
    if sama is None:
        print("oops! can't find FN111 for: " + str(record))
    else:
        x["sama"] = sama
        x["atytm0"] = time_or_none(x["atytm0"])
        x["atytm1"] = time_or_none(x["atytm1"])
        x["atycnt"] = int_or_none(x["atycnt"], 0)
        x["chkcnt"] = int_or_none(x["chkcnt"], 0)
        x["itvcnt"] = int_or_none(x["itvcnt"], 0)
        atytm0 = x.get("atytm0").strftime("%H:%M") if x.get("atytm0") else ""
        slug = "-".join([prj_cd, _sama, atytm0])
        x["slug"] = slugify(slug)

        item = FN112(**x)
        # item.save()
        objects.append(item)
FN112.objects.bulk_create(objects)
print("Done adding FN112 records.")


# ==================================
#    FN121  - Interviews

sql = """SELECT prj_cd, sam, sama, itvseq, itvtm0, area, [date],
         efftm0, efftm1, effcmp, effdur, mode, persons, anglers,
         rods, angmeth, angvis, angorig, angop1, angop2, angop3,
         comment1 from FN121"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:

    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    yr = datetime.strptime(prj_cd[6:8], "%y").year
    my_date = datetime.strptime(x["date"], "%Y-%m-%d")
    my_date = my_date.replace(year=yr)

    creel = FN011_cache.get(prj_cd)
    mode_code = x.pop("mode")
    mode = FN028_cache[prj_cd][mode_code]
    area_code = x.pop("area")
    area = FN026_cache[prj_cd][area_code]

    interview_time = time_or_none(x["efftm0"])

    # this is accomodate the project where sama wasn't populated
    # if it is null, we will figure out what it should have been:
    _sama = x.get("sama")
    if _sama:
        sama = FN111_cache[prj_cd][_sama]
    else:
        sama = (
            FN111.objects.filter(
                mode=mode,
                creel=creel,
                area=area,
                date=my_date,
                samtm0__lte=interview_time,
            )
            .order_by("samtm0")
            .first()
        )

    # related objects
    # x['creel'] = creel
    x["sama"] = sama
    # x['mode'] = mode
    # x['area'] = area

    # data conversion
    x["date"] = my_date
    x["efftm0"] = time_or_none(x["efftm0"])
    x["efftm1"] = time_or_none(x["efftm1"])
    x["itvseq"] = int_or_none(x["itvseq"])
    x["itvtm0"] = time_or_none(x["itvtm0"])
    x["effcmp"] = bool_or_none(x["effcmp"])
    x["effdur"] = float_or_none(x["effdur"])
    x["persons"] = int_or_none(x["persons"])
    x["anglers"] = int_or_none(x["anglers"])
    x["rods"] = int_or_none(x["rods"])
    x["angmeth"] = int_or_none(x["angmeth"])
    x["angvis"] = int_or_none(x["angvis"])
    x["angorig"] = int_or_none(x["angorig"])
    x["angop1"] = int_or_none(x["angop1"])
    x["angop2"] = int_or_none(x["angop2"])
    x["angop3"] = int_or_none(x["angop3"])

    slug = "-".join([prj_cd, x["sam"]])
    x["slug"] = slugify(slug)

    item = FN121(**x)
    # item.save()
    objects.append(item)

FN121.objects.bulk_create(objects)
print("Done adding FN121 records.")


FN121_cache = get_FN121_cache()


# ==================================
#    FN123  - Catch Counts

species_cache = {x.spc: x for x in Species.objects.all()}

sql = """select prj_cd, sam, spc, '00' as grp, sek, hvscnt, rlscnt, mescnt,
         meswt from fn123 order by prj_cd, sam, spc, sek"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    sam = x.pop("sam")
    spc = x.pop("spc")

    interview = FN121_cache[prj_cd][sam]
    species = species_cache[spc]
    # interview = FN121.objects.get(sama__creel__prj_cd=prj_cd, sam=sam)
    # species = Species.objects.get(species_code=spc)
    # related objects
    x["interview"] = interview
    x["species"] = species

    x["sek"] = bool_or_none(x["sek"])
    x["hvscnt"] = int_or_none(x["hvscnt"], 0)
    x["rlscnt"] = int_or_none(x["rlscnt"], 0)
    x["mescnt"] = int_or_none(x["mescnt"], 0)
    x["meswt"] = float_or_none(x["meswt"])

    slug = "-".join([prj_cd, sam, spc, x["grp"]])
    x["slug"] = slugify(slug)

    item = FN123(**x)
    # item.save()
    objects.append(item)

FN123.objects.bulk_create(objects)

print("Checking for fish with grp other than 00:")


sql = "select distinct grp from fn125 where GRP<>'00';"
cursor.execute(sql)
rs = cursor.fetchall()

if len(rs):
    grps = ", ".join([x[0] for x in rs])
    print("Oh-oh! - other group codes found in FN125 ({})".format(grps))

    # if any groups other than 00 are found in the FN125 table
    # repeat the prevous block of code using this sql statement which will
    # create teh missing FN123 records for these other group codes:

sql = """SELECT prj_cd,
       sam,
       grp,
       spc,
       '0' as sek,
       count(fish) AS HVSCNT,
       null as rlscnt,
       count(fish) AS MESCNT,
       null as meswt
  FROM fn125
 GROUP BY prj_Cd,
          sam,
          grp,
          spc
HAVING grp <> '00';
"""


print("Done adding FN123 records.")


FN123_cache = get_FN123_cache()

# ==================================
#    FN125  - Bio-Samples


sql = """select prj_cd, sam, spc, grp, fish, flen, tlen, rwt, sex,
         gon, null as mat, age, agest, clipc from fn125 order by
         prj_cd, sam, spc, grp, fish"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    sam = x.pop("sam")
    spc = x.pop("spc")
    grp = x.pop("grp")
    key = "{}-{}-{}-{}".format(prj_cd, sam, grp, spc)
    catch = FN123_cache.get(key)
    if catch is None:
        print("Unable to find catch record for {}".format(key))
        continue
    # related objects
    x["catch"] = catch

    x["flen"] = int_or_none(x["flen"])
    x["tlen"] = int_or_none(x["tlen"])
    x["rwt"] = int_or_none(x["rwt"])
    x["sex"] = int_or_none(x["sex"])
    x["gon"] = int_or_none(x["gon"])
    x["mat"] = int_or_none(x["mat"])
    x["age"] = int_or_none(x["age"])

    slug = "-".join([prj_cd, sam, spc, grp, x["fish"]])
    x["slug"] = slugify(slug)

    item = FN125(**x)
    # item.save()
    objects.append(item)

FN125.objects.bulk_create(objects)
print("Done adding FN125 records.")


FN125_cache = get_FN125_cache()


# ==================================
#    FN125_Tag

# (Note - the tagdocs that are null are replaced with 99999 - these
# should be updated someday.)


sql = """
SELECT prj_cd,
       sam,
       spc,
       grp,
       fish,
       1 as fish_tag_id,
       replace(fn125.tagid,"-","") as tagid,
       ifnull(fn125.tagdoc, '99999') as tagdoc,
       'C' as tagstat
  FROM fn125
 WHERE tagid IS NOT NULL AND
       tagid IS NOT '' and tagid not in ('5notag', '5NOTAG');"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    sam = x.pop("sam")
    spc = x.pop("spc")
    grp = x.pop("grp")
    fish = x.pop("fish")
    key = "{}-{}-{}-{}-{}".format(prj_cd, sam, spc, grp, int(fish))
    fish = FN125_cache.get(key)
    if fish is None:
        print("Unable to find fish record for {}".format(key))
        continue
    # related objects
    x["fish"] = fish

    item = FN125_Tag(**x)
    item.save()


print("Done adding FN125_Tag records.")


# ==================================
#    FN125_Lamprey


sql = """
SELECT prj_cd,
       sam,
       grp,
       spc,
       fish,
       1 as lamid,
       xlam
  FROM fn125;
"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    sam = x.pop("sam")
    spc = x.pop("spc")
    grp = x.pop("grp")
    fish = x.pop("fish")
    key = "{}-{}-{}-{}-{}".format(prj_cd, sam, spc, grp, int(fish))
    fish = FN125_cache.get(key)
    if fish is None:
        print("Unable to find fish record for {}".format(key))
        continue
    # related objects
    x["fish"] = fish

    slug = "-".join([key, "1"])
    x["slug"] = slugify(slug)

    item = FN125_Lamprey(**x)
    objects.append(item)

FN125_Lamprey.objects.bulk_create(objects)

print("Done adding FN125_Lamprey records.")


##
##
##
##  #==================================
##  #    FN127  - Age Estimates
##
##  SKIPPED FOR NOW
##
##  sql = """select prj_cd, sam, spc, grp, fish, ageid,
##           agea, agemt, conf, edge, nca from fn127
##           order by prj_cd, sam, spc, grp, fish, ageid;"""
##
##  cursor.execute(sql)
##  rs = cursor.fetchall()
##  col_names = [x[0].lower() for x in cursor.description]
##  objects = []
##
##  for record in rs:
##
##      x = {k:v for k,v in zip(col_names, record)}
##      prj_cd = x.pop('prj_cd')
##      sam = x.pop('sam')
##      spc = x.pop('spc')
##      grp = x.pop('grp')
##      fish = x.pop('fish')
##
##      fish = FN125.objects.get(catch__interview__creel__prj_cd=prj_cd,
##                                catch__interview__sam=sam,
##                                catch__species__species_code=spc,
##                               fish=fish, grp=grp)
##
##      x['fish'] = fish
##      x['ageid'] = int_or_none(x['ageid'])
##      x['agea'] = int_or_none(x['agea'])
##      x['conf'] = int_or_none(x['conf'])
##      x['nca'] = int_or_none(x['nca'])
##
##      item = FN127(**x)
##      objects.append(item)
##
##  FN127.objects.bulk_create(objects)
##  print("Done adding FN127 records.")
##


# ==================================
#    FR711  - Effort Estimates

FR711_cache = {}
items = FR711.objects.all().select_related("creel")
for item in items:
    key = "{}-{}".format(item.creel.prj_cd, item.run)
    FR711_cache[key] = item


strata_cache = {}
items = Strata.objects.all().select_related("creel_run", "creel_run__creel")
for item in items:
    key = "{}-{}-{}".format(
        item.creel_run.creel.prj_cd, item.creel_run.run, item.stratum_label
    )
    strata_cache[key] = item


sql = """
SELECT prj_cd,
       run,
       rec_tp,
       strat,
       strat_days,
       sam_days,
       strat_hrs as strat_hours,
       sam_hrs as sam_hours,
       fpc,
       prd_dur,
       atyunit,
       chkflag,
       strat1,
       strat_nn
  FROM FR712
  order by prj_cd, run, rec_tp, strat;
"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    run = x.pop("run")
    key = "{}-{}".format(prj_cd, run)
    fr711 = FR711_cache.get(key)
    if fr711 is None:
        print("unable to find {}".format(key))
        continue

    stratum_code = x.pop("strat")

    key = "{}-{}-{}".format(prj_cd, run, stratum_code)
    stratum = strata_cache.get(key)

    if stratum is None:
        print("unable to find {}".format(key))
        continue

    x["stratum"] = stratum

    x["rec_tp"] = int_or_none(x["rec_tp"])

    x["strat_days"] = int_or_none(x["strat_days"])
    x["sam_days"] = int_or_none(x["sam_days"])
    x["strat_hours"] = float_or_none(x["strat_hours"])
    x["sam_hours"] = float_or_none(x["sam_hours"])
    # x["fpc"] = float_or_none(x["fpc"])
    x["fpc"] = x.get("fpc") if x.get("fpc") else 0.0
    x["prd_dur"] = float_or_none(x["prd_dur"])
    x["atyunit"] = int_or_none(x["atyunit"])
    x["chkflag"] = int_or_none(x["chkflag"])
    x["strat_nn"] = int_or_none(x["strat_nn"])

    # strat days is 0 or greater, not null
    # strat hours is 0 or greater, not null
    # sam days can be null
    # sam hours can be null
    # fpc can be null
    # atyunit can be null
    # chkflag can be null
    # strat1 can be null
    # strat_nn not be null

    item = FR712(**x)
    objects.append(item)

FR712.objects.bulk_create(objects)
print("Done adding FR712 records.")


# ==================================
#    FR713  - Effort Estimates


sql = """ SELECT PRJ_CD,
       RUN,
       STRAT,
       REC_TP,
       DATE,
       ANGLER_MN,
       ANGLER_S,
       ANGLER_SS,
       ATY0,
       ATY1,
       ATY1_SE,
       ATY1_VR,
       ATY2,
       ATY2_SE,
       ATY2_VR,
       ATYCNT_S,
       ATY_DAYS,
       ATY_HRS,
       ATY_NN,
       CHKCNT_S,
       CIF_NN,
       EFFAE,
       EFFAE_SE,
       EFFAE_VR,
       EFFAO_S,
       EFFAO_SS,
       EFFPE,
       EFFPE_SE,
       EFFPE_VR,
       EFFPO_S,
       EFFPO_SS,
       EFFRE,
       EFFRE_SE,
       EFFRE_VR,
       EFFRO_S,
       EFFRO_SS,
       ITVCNT_S,
       PERSON_S,
       ROD_MNA,
       ROD_S,
       ROD_SS,
       TRIPNE,
       TRIPNE_SE,
       TRIPNE_VR,
       TRIPNO
  FROM FR713
 ORDER BY PRJ_CD,
          RUN,
          STRAT,
          REC_TP,
          DATE;"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k: v for k, v in zip(col_names, record)}
    prj_cd = x.pop("prj_cd")
    stratum_code = x.pop("strat")
    run = x.pop("run")
    rec_tp = x.pop("rec_tp")

    yr = datetime.strptime(prj_cd[6:8], "%y").year

    key = "{}-{}-{}-{}".format(prj_cd, run, rec_tp, stratum_code)
    fr712 = FR712_cache.get(key)
    if fr712 is None:
        print("unable to find {}".format(key))
        continue

    x["fr712"] = fr712

    if x.get("date"):
        if x.get("date") == "":
            x["date"] = None
        else:
            my_date = datetime.strptime(x["date"], "%Y-%m-%d")
            my_date = my_date.replace(year=yr)
            x["date"] = my_date

    # x['run'] = int_or_none(x['run'])
    # x["rec_tp"] = int_or_none(x["rec_tp"])
    x["angler_mn"] = float_or_none(x["angler_mn"])
    x["angler_s"] = int_or_none(x["angler_s"])
    x["angler_ss"] = int_or_none(x["angler_ss"])
    x["aty0"] = float_or_none(x["aty0"])
    x["aty1"] = float_or_none(x["aty1"])
    x["aty1_se"] = float_or_none(x["aty1_se"])
    x["aty1_vr"] = float_or_none(x["aty1_vr"])
    x["aty2"] = float_or_none(x["aty2"])
    x["aty2_se"] = float_or_none(x["aty2_se"])
    x["aty2_vr"] = float_or_none(x["aty2_vr"])
    x["atycnt_s"] = int_or_none(x["atycnt_s"])
    x["aty_days"] = int_or_none(x["aty_days"])
    x["aty_hrs"] = float_or_none(x["aty_hrs"])
    x["aty_nn"] = int_or_none(x["aty_nn"])
    x["chkcnt_s"] = int_or_none(x["chkcnt_s"])
    x["cif_nn"] = int_or_none(x["cif_nn"])
    x["effae"] = float_or_none(x["effae"])
    x["effae_se"] = float_or_none(x["effae_se"])
    x["effae_vr"] = float_or_none(x["effae_vr"])
    x["effao_s"] = float_or_none(x["effao_s"])
    x["effao_ss"] = float_or_none(x["effao_ss"])
    x["effpe"] = float_or_none(x["effpe"])
    x["effpe_se"] = float_or_none(x["effpe_se"])
    x["effpe_vr"] = float_or_none(x["effpe_vr"])
    x["effpo_s"] = float_or_none(x["effpo_s"])
    x["effpo_ss"] = float_or_none(x["effpo_ss"])
    x["effre"] = float_or_none(x["effre"])
    x["effre_se"] = float_or_none(x["effre_se"])
    x["effre_vr"] = float_or_none(x["effre_vr"])
    x["effro_s"] = float_or_none(x["effro_s"])
    x["effro_ss"] = float_or_none(x["effro_ss"])
    x["itvcnt_s"] = int_or_none(x["itvcnt_s"])
    x["person_s"] = int_or_none(x["person_s"])
    x["rod_mna"] = float_or_none(x["rod_mna"])
    x["rod_s"] = int_or_none(x["rod_s"])
    x["rod_ss"] = int_or_none(x["rod_ss"])
    x["tripne"] = float_or_none(x["tripne"])
    x["tripne_se"] = float_or_none(x["tripne_se"])
    x["tripne_vr"] = float_or_none(x["tripne_vr"])
    x["tripno"] = int_or_none(x["tripno"])

    item = FR713(**x)
    objects.append(item)

FR713.objects.bulk_create(objects)
print("Done adding FR713 records.")


# ==================================
#    FR714  - Catch Estimates


# sql = """select prj_cd, strat, spc, sek, [date], rod1_s, angler1_s,
#         catno1_s, catno1_ss, catno_s, catno_ss, cif1_nn, hvsno1_s,
#         hvsno1_ss, hvsno_s, hvsno_ss, mescnt_s, rec_tp, [run] from fr714
#         order by prj_cd, strat, spc, sek;"""

sql = """SELECT PRJ_CD,
       RUN,
       STRAT,
       REC_TP,
       DATE,
       SPC,
       SEK,
       ANGLER1_S,
       CATEA1_XY,
       CATEA_XY,
       CATEP1_XY,
       CATEP_XY,
       CATER1_XY,
       CATER_XY,
       CATNE,
       CATNE1,
       CATNE1_PC,
       CATNE1_SE,
       CATNE1_VR,
       CATNE_SE,
       CATNE_VR,
       CATNO1_S,
       CATNO1_SS,
       CATNO_S,
       CATNO_SS,
       CIF1_NN,
       CUENAE,
       CUENAE1,
       CUENAO,
       CUENAO1,
       EFFAE1,
       EFFAE1_PC,
       EFFAE1_SE,
       EFFAE1_VR,
       EFFAO1_S,
       EFFAO1_SS,
       EFFPE1,
       EFFPE1_SE,
       EFFPE1_VR,
       EFFPO1_S,
       EFFPO1_SS,
       EFFRE1,
       EFFRE1_SE,
       EFFRE1_VR,
       EFFRO1_S,
       EFFRO1_SS,
       HVSCAT_PC,
       HVSEA1_XY,
       HVSEA_XY,
       HVSEP1_XY,
       HVSEP_XY,
       HVSER1_XY,
       HVSER_XY,
       HVSNE,
       HVSNE1,
       HVSNE1_SE,
       HVSNE1_VR,
       HVSNE_SE,
       HVSNE_VR,
       HVSNO1_S,
       HVSNO1_SS,
       HVSNO_S,
       HVSNO_SS,
       MESCNT_S,
       MESWT_S,
       ROD1_S
  FROM fr714
 ORDER BY PRJ_CD,
          RUN,
          DATE,
          STRAT,
          REC_TP,
          SPC,
          SEK
"""


cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k: v for k, v in zip(col_names, record)}

    prj_cd = x.pop("prj_cd")
    stratum_code = x.pop("strat")
    run = x.pop("run")
    rec_tp = x.pop("rec_tp")

    yr = datetime.strptime(prj_cd[6:8], "%y").year

    key = "{}-{}-{}-{}".format(prj_cd, run, rec_tp, stratum_code)
    fr712 = FR712_cache.get(key)
    if fr712 is None:
        print("unable to find {}".format(key))
        continue

    x["fr712"] = fr712

    spc = x.pop("spc")
    species = species_cache.get(spc)
    x["species"] = species

    if x.get("date"):
        if x.get("date") == "":
            x["date"] = None
        else:
            my_date = datetime.strptime(x["date"], "%Y-%m-%d")
            my_date = my_date.replace(year=yr)
            x["date"] = my_date

    #    x['run'] = int_or_none(x['run'])
    # x["rec_tp"] = int_or_none(x["rec_tp"])
    x["sek"] = bool_or_none(x["sek"])
    x["angler1_s"] = int_or_none(x["angler1_s"])
    x["catea1_xy"] = float_or_none(x["catea1_xy"])
    x["catea_xy"] = float_or_none(x["catea_xy"])
    x["catep1_xy"] = float_or_none(x["catep1_xy"])
    x["catep_xy"] = float_or_none(x["catep_xy"])
    x["cater1_xy"] = float_or_none(x["cater1_xy"])
    x["cater_xy"] = float_or_none(x["cater_xy"])
    x["catne"] = float_or_none(x["catne"])
    x["catne1"] = float_or_none(x["catne1"])
    x["catne1_pc"] = float_or_none(x["catne1_pc"])
    x["catne1_se"] = float_or_none(x["catne1_se"])
    x["catne1_vr"] = float_or_none(x["catne1_vr"])
    x["catne_se"] = float_or_none(x["catne_se"])
    x["catne_vr"] = float_or_none(x["catne_vr"])
    x["catno1_s"] = int_or_none(x["catno1_s"])
    x["catno1_ss"] = int_or_none(x["catno1_ss"])
    x["catno_s"] = int_or_none(x["catno_s"])
    x["catno_ss"] = int_or_none(x["catno_ss"])
    x["cif1_nn"] = int_or_none(x["cif1_nn"])
    x["cuenae"] = float_or_none(x["cuenae"])
    x["cuenae1"] = float_or_none(x["cuenae1"])
    x["cuenao"] = float_or_none(x["cuenao"])
    x["cuenao1"] = float_or_none(x["cuenao1"])
    x["effae1"] = float_or_none(x["effae1"])
    x["effae1_pc"] = float_or_none(x["effae1_pc"])
    x["effae1_se"] = float_or_none(x["effae1_se"])
    x["effae1_vr"] = float_or_none(x["effae1_vr"])
    x["effao1_s"] = float_or_none(x["effao1_s"])
    x["effao1_ss"] = float_or_none(x["effao1_ss"])
    x["effpe1"] = float_or_none(x["effpe1"])
    x["effpe1_se"] = float_or_none(x["effpe1_se"])
    x["effpe1_vr"] = float_or_none(x["effpe1_vr"])
    x["effpo1_s"] = float_or_none(x["effpo1_s"])
    x["effpo1_ss"] = float_or_none(x["effpo1_ss"])
    x["effre1"] = float_or_none(x["effre1"])
    x["effre1_se"] = float_or_none(x["effre1_se"])
    x["effre1_vr"] = float_or_none(x["effre1_vr"])
    x["effro1_s"] = float_or_none(x["effro1_s"])
    x["effro1_ss"] = float_or_none(x["effro1_ss"])
    x["hvscat_pc"] = float_or_none(x["hvscat_pc"])
    x["hvsea1_xy"] = float_or_none(x["hvsea1_xy"])
    x["hvsea_xy"] = float_or_none(x["hvsea_xy"])
    x["hvsep1_xy"] = float_or_none(x["hvsep1_xy"])
    x["hvsep_xy"] = float_or_none(x["hvsep_xy"])
    x["hvser1_xy"] = float_or_none(x["hvser1_xy"])
    x["hvser_xy"] = float_or_none(x["hvser_xy"])
    x["hvsne"] = float_or_none(x["hvsne"])
    x["hvsne1"] = float_or_none(x["hvsne1"])
    x["hvsne1_se"] = float_or_none(x["hvsne1_se"])
    x["hvsne1_vr"] = float_or_none(x["hvsne1_vr"])
    x["hvsne_se"] = float_or_none(x["hvsne_se"])
    x["hvsne_vr"] = float_or_none(x["hvsne_vr"])
    x["hvsno1_s"] = int_or_none(x["hvsno1_s"])
    x["hvsno1_ss"] = int_or_none(x["hvsno1_ss"])
    x["hvsno_s"] = int_or_none(x["hvsno_s"])
    x["hvsno_ss"] = int_or_none(x["hvsno_ss"])
    x["mescnt_s"] = int_or_none(x["mescnt_s"])
    x["meswt_s"] = float_or_none(x["meswt_s"])
    x["rod1_s"] = int_or_none(x["rod1_s"])

    item = FR714(**x)
    objects.append(item)

FR714.objects.bulk_create(objects)
print("Done adding FR714 records.")


# ==================================
#    FR715  - ANGLER OPTIONS


# sql = """select prj_cd, strat, spc, sek, [date], rod1_s, angler1_s,
#         catno1_s, catno1_ss, catno_s, catno_ss, cif1_nn, hvsno1_s,
#         hvsno1_ss, hvsno_s, hvsno_ss, mescnt_s, rec_tp, [run] from fr714
#         order by prj_cd, strat, spc, sek;"""

sql = """
SELECT prj_cd,
       run,
       rec_tp,
       strat,
       ang_fn,
       ang_val,
       ang_freq,
       ang_prop,
       pty_freq,
       pty_prop
  FROM FR715
 ORDER BY prj_cd,
          run,
          rec_tp,
          strat,
          ang_fn,
          ang_val;
"""


cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k: v for k, v in zip(col_names, record)}

    prj_cd = x.pop("prj_cd")
    stratum_code = x.pop("strat")
    run = x.pop("run")
    rec_tp = x.pop("rec_tp")

    key = "{}-{}-{}-{}".format(prj_cd, run, rec_tp, stratum_code)
    fr712 = FR712_cache.get(key)
    if fr712 is None:
        print("unable to find {}".format(key))
        continue

    x["fr712"] = fr712

    # x["ang_val"] = int_or_none(x["ang_val"])
    x["ang_freq"] = int_or_none(x["ang_freq"])
    x["ang_prop"] = float_or_none(x["ang_prop"])
    x["pty_freq"] = int_or_none(x["pty_freq"])
    x["pty_prop"] = float_or_none(x["pty_prop"])

    item = FR715(**x)
    objects.append(item)

FR715.objects.bulk_create(objects)
print("Done adding FR715 records.")


conn.commit()

# clean up
cur.close()
conn.close()
