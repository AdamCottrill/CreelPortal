'''
=============================================================
 /home/adam/Documents/djcode/creel_portal/utils/migrate_ls_sc_data.py
 Created: 11 Feb 2017 15:40:28


 DESCRIPTION:



 A. Cottrill
=============================================================
'''



import django
import os

os.chdir('./..')
django.setup()



import django_settings
import sqlite3

from creel_portal.models import *

from utils.helper_fcts import *


#SRC_DB = '/home/adam/Documents/work/Superior/SC_master.db'
#SRC_DB = '/home/adam/Documents/work/Superior/lhmu_sc_warehouse.db'
SRC_DB = 'C:/1work/ScrapBook/lhmu_sc_warehouse_clean.db'

conn = sqlite3.connect(SRC_DB)
cursor = conn.cursor()

#lake = Lake(lake_name='Huron', abbrev='HU')
#lake.save()

lake = Lake.objects.get(abbrev='HU')
print("Working on Lake " + str(lake))
#==================================
#    FN011  - Project Details

sql = """select PRJ_CD, ARU, COMMENT0, FOF_LOC, FOF_NM, PRJ_DATE0,
         PRJ_DATE1, PRJ_HIS, PRJ_LDR, PRJ_NM, PRJ_SIZE, PRJ_VER,
         V0, WBY WBY_NM from fn011;"""

cursor.execute(sql)
rs = cursor.fetchall()

col_names = [x[0].lower() for x in cursor.description]
#projects must be created individually as they have save()
# method that generates a slug
for record in rs:
    x = {k:v for k,v in zip(col_names, record)}
    x['lake'] = lake
    yr = datetime.strptime(x['prj_cd'][6:8],'%y').year
    x['year'] = yr
    prj_date0 = datetime.strptime(x['prj_date0'],'%Y-%m-%d')
    prj_date1 = datetime.strptime(x['prj_date1'],'%Y-%m-%d')
    x['prj_date0'] = prj_date0.replace(year=yr)
    x['prj_date1'] = prj_date1.replace(year=yr)
    x['prj_cd'] = x['prj_cd']
    creel = FN011(**x)
    creel.save()
print("Done adding FN011 records.")

#==================================
#  FN022 - Temporal/Seasonal Strata:

sql = """SELECT PRJ_CD, SSN, SSN_DATE0, SSN_DATE1, SSN_DES
         from fn022;"""
cursor.execute(sql)
rs = cursor.fetchall()
objects = []
col_names = [x[0].lower() for x in cursor.description]
for record in rs:
    x = {k:v for k,v in zip(col_names, record)}

    yr = datetime.strptime(x['prj_cd'][6:8],'%y').year
    ssn_date0 = datetime.strptime(x['ssn_date0'],'%Y-%m-%d')
    ssn_date1 = datetime.strptime(x['ssn_date1'],'%Y-%m-%d')
    x['ssn_date0'] = ssn_date0.replace(year=yr)
    x['ssn_date1'] = ssn_date1.replace(year=yr)
    prj_cd = x.pop('prj_cd')
    x['creel'] = FN011.objects.get(prj_cd=prj_cd)

    item = FN022(**x)
    #item.save()
    objects.append(item)

FN022.objects.bulk_create(objects)
print("Done adding FN022 records.")


#==================================
#    FN023 -  Day Types Strata

sql = """SELECT PRJ_CD, SSN, DOW_LST, DTP, DTP_NM from FN023;"""
cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    ssn = x.pop('ssn')
    season = FN022.objects.filter(creel__prj_cd=prj_cd,
                               ssn=ssn).get()
    x['season'] = season
    item = FN023(**x)
    #item.save()
    objects.append(item)
FN023.objects.bulk_create(objects)


print("Done adding FN023 records.")


#==================================
#    FN024 - Periods

sql = """SELECT PRJ_CD, SSN, DTP, PRD, PRDTM0, PRDTM1 from FN024;"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    ssn = x.pop('ssn')
    dtp = x.pop('dtp')

    daytype = FN023.objects.filter(season__creel__prj_cd=prj_cd,
                               season__ssn=ssn, dtp=dtp).get()
    x['daytype'] = daytype
    x['prdtm0'] = datetime.strptime(x['prdtm0'],'%H:%M')
    x['prdtm1'] = datetime.strptime(x['prdtm1'],'%H:%M')
    item = FN024(**x)
    #item.save()
    objects.append(item)
FN024.objects.bulk_create(objects)
print("Done adding FN024 records.")


#==================================
#     FN025 - Exception Dates

sql = """SELECT PRJ_CD, [DATE], DTP1 from FN025;"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    yr = datetime.strptime(prj_cd[6:8],'%y').year
    my_date = datetime.strptime(x['date'],'%Y-%m-%d')
    my_date = my_date.replace(year=yr)
    season = FN022.objects.filter(ssn_date0__lte=my_date)\
             .filter(ssn_date1__gte=my_date)\
             .filter(creel__prj_cd=prj_cd).get()
    x['season'] = season
    x['date'] = my_date
    item = FN025(**x)
    #item.save()
    objects.append(item)
FN025.objects.bulk_create(objects)
print("Done adding FN025 records.")


#==================================
#  FN026  - Spatial Strata

sql = """SELECT prj_cd, space, space_des, space_siz, area_cnt,
         area_lst, area_wt from FN026;"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    x['creel'] = FN011.objects.get(prj_cd=prj_cd)
    x['space_siz'] = int_or_none(x['space_siz'])
    x['area_cnt'] = int_or_none(x['area_cnt'])
    x['area_wt'] = int_or_none(x['area_wt'])
    item = FN026(**x)
    #item.save()
    objects.append(item)
FN026.objects.bulk_create(objects)
print("Done adding FN026 records.")



#==================================
#    FN028  - Fishing Modes

sql = """SELECT PRJ_CD, ATYUNIT, CHKFLAG, ITVUNIT, MODE,
         MODE_DES from FN028 where V0 <> '.++';"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    x['creel'] = FN011.objects.get(prj_cd=prj_cd)
    x['atyunit'] = int_or_none(x['atyunit'])
    x['itvunit'] = int_or_none(x['itvunit'])
    x['chkflag'] = int_or_none(x['chkflag'])
    item = FN028(**x)
    #item.save()
    objects.append(item)
FN028.objects.bulk_create(objects)
print("Done adding FN028 records.")


#==================================
#          FR711

#the FR711 table holds the settings for the analysis -
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
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    try:
        x['creel'] = FN011.objects.get(prj_cd=prj_cd)
    except:
        msg = "{} not found.".format(prj_cd)
        continue
    item = FR711(**x)
    #item.save()
    objects.append(item)
FR711.objects.bulk_create(objects)
print("Done adding FR711 records.")


#==================================
#          STRATA

#now we need to build the strata for each project from the design tables and the
# strat_mask in the FR711 table:

fr711s = FR711.objects.all()

all_strata = []
for creel_run in fr711s:
    combined_strata = get_combined_strata(creel_run)
    all_strata.extend(combined_strata)
    other_strata = get_strata(creel_run)
    all_strata.extend(other_strata)

objects = []
col_names = ['creel_run_id', 'stratum_label', 'season_id',
             'area_id', 'daytype_id', 'period_id', 'mode_id']

for x in all_strata:
    x = {k:v for k,v in zip(col_names, x)}
    item = Strata(**x)
    objects.append(item)
Strata.objects.bulk_create(objects)
print("Done adding Strata records.")



#==================================
#    FN111  - Interview Logs

sql = """SELECT prj_cd, sama, [date], samtm0, area, mode,
         weather, comment1 from FN111"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:

    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    yr = datetime.strptime(prj_cd[6:8],'%y').year
    my_date = datetime.strptime(x['date'],'%Y-%m-%d')
    my_date = my_date.replace(year=yr)
    my_time = datetime.strptime(x['samtm0'],'%H:%M').time()

    x['date'] = my_date
    x['samtm0'] = my_time

    creel = FN011.objects.get(prj_cd=prj_cd)
    x['creel'] = creel

    season = FN022.objects.filter(creel__prj_cd=prj_cd).\
             filter(ssn_date0__lte = my_date).\
             filter(ssn_date1__gte = my_date).get()
    x['season'] = season

    my_dow = int(datetime.strftime(my_date, '%w')) + 1
    daytype = FN023.objects.filter(season=season).\
              filter(dow_lst__contains=str(my_dow)).get()
    x['daytype'] = daytype

    period = FN024.objects.filter(daytype=daytype).\
             filter(prdtm0__lte = my_time, prdtm1__gt = my_time).get()
    x['period'] = period

    exception_date = FN025.objects.filter(season=season, date=my_date).first()
    if exception_date:
        x['daycode'] = exception_date.dtp1
    else:
        x['daycode'] = daytype.dtp

    area_code = x['area']
    area = FN026.objects.get(creel=creel, space=area_code)
    x['area'] = area

    mode_code = x['mode']
    mode = FN028.objects.get(creel=creel, mode=mode_code)
    x['mode'] = mode

    item = FN111(**x)
    #item.save()
    objects.append(item)
FN111.objects.bulk_create(objects)
print("Done adding FN111 records.")



#==================================
#    FN112  - ActivityCounts

sql = """select prj_cd, sama, atytm0, atytm1, atycnt, chkcnt,
         itvcnt from fn112 order by prj_cd, sama"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    sama = x.pop('sama')
    sama = FN111.objects.filter(creel__prj_cd=prj_cd,
                                sama=sama).get()
    if sama is None:
        print("oops! can't find FN111 for: " + str(record))
    else:
        x['sama'] = sama
        x['atytm0'] = time_or_none(x['atytm0'])
        x['atytm1'] = time_or_none(x['atytm1'])
        x['atycnt'] = int_or_none(x['atycnt'], 0)
        x['chkcnt'] = int_or_none(x['chkcnt'], 0)
        x['itvcnt'] = int_or_none(x['itvcnt'], 0)
        item = FN112(**x)
        #item.save()
        objects.append(item)
FN112.objects.bulk_create(objects)
print("Done adding FN112 records.")



#==================================
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

    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    yr = datetime.strptime(prj_cd[6:8],'%y').year
    my_date = datetime.strptime(x['date'],'%Y-%m-%d')
    my_date = my_date.replace(year=yr)

    creel = FN011.objects.get(prj_cd=prj_cd)
    mode_code = x.pop('mode')
    mode = FN028.objects.get(creel=creel, mode=mode_code)
    area_code = x.pop('area')
    area = FN026.objects.get(creel=creel, area_lst=area_code)

    interview_time = time_or_none(x['efftm0'])

    # this is accomodate the project where sama wasn't populated
    # if it is null, we will figure out what it should have been:
    _sama = x.get('sama')
    if _sama:
        sama = FN111.objects.get(creel=creel, sama=_sama)
    else:
        sama =  FN111.objects.filter(mode=mode, creel=creel,
                                     area=area, date=my_date,
                                     samtm0__lte=interview_time).\
                                     order_by('samtm0').first()

    #related objects
    #x['creel'] = creel
    x['sama'] = sama
    #x['mode'] = mode
    #x['area'] = area

    #data conversion
    x['date']=  my_date
    x['efftm0'] = time_or_none(x['efftm0'])
    x['efftm1'] = time_or_none(x['efftm1'])
    x['itvseq'] = int_or_none(x['itvseq'])
    x['itvtm0'] = time_or_none(x['itvtm0'])
    x['effcmp'] = bool_or_none(x['effcmp'])
    x['effdur'] = float_or_none(x['effdur'])
    x['persons'] = int_or_none(x['persons'])
    x['anglers'] = int_or_none(x['anglers'])
    x['rods'] = int_or_none(x['rods'])
    x['angmeth'] = int_or_none(x['angmeth'])
    x['angvis'] = int_or_none(x['angvis'])
    x['angorig'] = int_or_none(x['angorig'])
    x['angop1'] = int_or_none(x['angop1'])
    x['angop2'] = int_or_none(x['angop2'])
    x['angop3'] = int_or_none(x['angop3'])

    item = FN121(**x)
    #item.save()
    objects.append(item)

FN121.objects.bulk_create(objects)
print("Done adding FN121 records.")




#==================================
#    FN123  - Catch Counts

sql = """select prj_cd, sam, spc, sek, hvscnt, rlscnt, mescnt,
         meswt from fn123 order by prj_cd, sam, spc, sek"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []
for record in rs:
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    sam = x.pop('sam')
    spc = x.pop('spc')

    interview = FN121.objects.get(sama__creel__prj_cd=prj_cd, sam=sam)
    species = Species.objects.get(species_code=spc)
    #related objects
    x['interview'] = interview
    x['species'] = species

    x['sek'] = bool_or_none(x['sek'])
    x['hvscnt'] = int_or_none(x['hvscnt'], 0)
    x['rlscnt'] = int_or_none(x['rlscnt'], 0)
    x['mescnt'] = int_or_none(x['mescnt'], 0)
    x['meswt'] = float_or_none(x['meswt'])

    item = FN123(**x)
    #item.save()
    objects.append(item)

FN123.objects.bulk_create(objects)
print("Done adding FN123 records.")


##  #==================================
##  #    FN125  - Bio-Samples
##
##  SKIPPED FOR NOW
##
##  sql = """select prj_cd, sam, spc, grp, fish, flen, tlen, rwt, sex,
##           gon, null as mat, age, agest, clipc, fate from fn125 order by
##           prj_cd, sam, spc, grp, fish"""
##
##  cursor.execute(sql)
##  rs = cursor.fetchall()
##  col_names = [x[0].lower() for x in cursor.description]
##  objects = []
##
##  for record in rs:
##      x = {k:v for k,v in zip(col_names, record)}
##      prj_cd = x.pop('prj_cd')
##      sam = x.pop('sam')
##      spc = x.pop('spc')
##
##      catch = FN123.objects.get(interview__creel__prj_cd=prj_cd,
##                                interview__sam=sam,
##                                species__species_code=spc)
##      #related objects
##      x['catch'] = catch
##
##      x['flen'] = int_or_none(x['flen'])
##      x['tlen'] = int_or_none(x['tlen'])
##      x['rwt'] = int_or_none(x['rwt'])
##      x['sex'] = int_or_none(x['sex'])
##      x['gon'] = int_or_none(x['gon'])
##      x['mat'] = int_or_none(x['mat'])
##      x['age'] = int_or_none(x['age'])
##
##      item = FN125(**x)
##      #item.save()
##      objects.append(item)
##
##  FN125.objects.bulk_create(objects)
##  print("Done adding FN125 records.")
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




#==================================
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
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    stratum_code = x.pop('strat')
    run = x.pop('run')

    yr = datetime.strptime(prj_cd[6:8],'%y').year

    #stratum = Strata.objects.filter(creel_run__creel__prj_cd=prj_cd).\
    #          filter(stratum_label=stratum_code, run=run).get()

    try:
        stratum = Strata.objects.filter(creel_run__creel__prj_cd=prj_cd).\
              filter(stratum_label=stratum_code, creel_run__run=run).get()
    except:
        print("Could not find strata for prj_cd:{} Strata:{} Run:{} ".
              format(prj_cd, stratum_code, run))
        next

#    creel = FN011.objects.get(prj_cd=prj_cd)
#    #get all of the related objects:
#    mode = creel.modes.filter(mode=stratum[9:]).first()
#    season = creel.seasons.filter(ssn=stratum[:2]).first()
#    if season:
#        daytype = season.daytypes.filter(dtp=stratum[3]).first()
#    else:
#        daytype = None
#    if daytype:
#        period = daytype.periods.filter(prd=stratum[4]).first()
#    else:
#        period = None
#
#    space = creel.spatial_strata.filter(space=stratum[6:8]).first()
#
#
#    x['creel'] = creel
#    x['mode'] = mode
#    x['season'] = season
#    x['period'] = period
#    x['dtp'] = daytype
#    x['area'] = space

    x['stratum'] = stratum

    if x.get('date'):
        if x.get('date') == '':
            x['date'] = None
        else:
            my_date = datetime.strptime(x['date'],'%Y-%m-%d')
            my_date = my_date.replace(year=yr)
            x['date'] = my_date

    #x['run'] = int_or_none(x['run'])
    x['rec_tp'] = int_or_none(x['rec_tp'])
    x['angler_mn'] = float_or_none(x['angler_mn'])
    x['angler_s'] = int_or_none(x['angler_s'])
    x['angler_ss']= int_or_none(x['angler_ss'])
    x['aty0'] = float_or_none(x['aty0'])
    x['aty1'] = float_or_none(x['aty1'])
    x['aty1_se'] = float_or_none(x['aty1_se'])
    x['aty1_vr'] = float_or_none(x['aty1_vr'])
    x['aty2'] = float_or_none(x['aty2'])
    x['aty2_se'] = float_or_none(x['aty2_se'])
    x['aty2_vr'] = float_or_none(x['aty2_vr'])
    x['atycnt_s']= int_or_none(x['atycnt_s'])
    x['aty_days']= int_or_none(x['aty_days'])
    x['aty_hrs'] = float_or_none(x['aty_hrs'])
    x['aty_nn']= int_or_none(x['aty_nn'])
    x['chkcnt_s']= int_or_none(x['chkcnt_s'])
    x['cif_nn']= int_or_none(x['cif_nn'])
    x['effae'] = float_or_none(x['effae'])
    x['effae_se'] = float_or_none(x['effae_se'])
    x['effae_vr'] = float_or_none(x['effae_vr'])
    x['effao_s'] = float_or_none(x['effao_s'])
    x['effao_ss'] = float_or_none(x['effao_ss'])
    x['effpe'] = float_or_none(x['effpe'])
    x['effpe_se'] = float_or_none(x['effpe_se'])
    x['effpe_vr'] = float_or_none(x['effpe_vr'])
    x['effpo_s'] = float_or_none(x['effpo_s'])
    x['effpo_ss'] = float_or_none(x['effpo_ss'])
    x['effre'] = float_or_none(x['effre'])
    x['effre_se'] = float_or_none(x['effre_se'])
    x['effre_vr'] = float_or_none(x['effre_vr'])
    x['effro_s'] = float_or_none(x['effro_s'])
    x['effro_ss'] = float_or_none(x['effro_ss'])
    x['itvcnt_s']= int_or_none(x['itvcnt_s'])
    x['person_s']= int_or_none(x['person_s'])
    x['rod_mna'] = float_or_none(x['rod_mna'])
    x['rod_s']= int_or_none(x['rod_s'])
    x['rod_ss'] = int_or_none(x['rod_ss'])
    x['tripne'] = float_or_none(x['tripne'])
    x['tripne_se'] = float_or_none(x['tripne_se'])
    x['tripne_vr'] = float_or_none(x['tripne_vr'])
    x['tripno'] = int_or_none(x['tripno'])

    item = FR713(**x)
    objects.append(item)

FR713.objects.bulk_create(objects)
print("Done adding FR713 records.")



#==================================
#    FR714  - Catch Estimates


#sql = """select prj_cd, strat, spc, sek, [date], rod1_s, angler1_s,
#         catno1_s, catno1_ss, catno_s, catno_ss, cif1_nn, hvsno1_s,
#         hvsno1_ss, hvsno_s, hvsno_ss, mescnt_s, rec_tp, [run] from fr714
#         order by prj_cd, strat, spc, sek;"""

sql = """SELECT PRJ_CD,
       RUN,
       DATE,
       STRAT,
       REC_TP,
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
    x = {k:v for k,v in zip(col_names, record)}

    prj_cd = x.pop('prj_cd')
    stratum_code = x.pop('strat')
    run = x.pop('run')

    yr = datetime.strptime(prj_cd[6:8],'%y').year

    try:
        stratum = Strata.objects.filter(creel_run__creel__prj_cd=prj_cd).\
              filter(stratum_label=stratum_code, creel_run__run=run).get()
    except:
        print("Could not find strata for prj_cd:{} Strata:{} Run:{} ".
              format(prj_cd, stratum_code, run))
        next

#    stratum = x.get('strat')
#
#    creel = FN011.objects.get(prj_cd=prj_cd)
#
#    mode = creel.modes.filter(mode=stratum[9:]).first()
#    season = creel.seasons.filter(ssn=stratum[:2]).first()
#    if season:
#        daytype = season.daytypes.filter(dtp=stratum[3]).first()
#    else:
#        daytype = None
#    if daytype:
#        period = daytype.periods.filter(prd=stratum[4]).first()
#    else:
#        period = None
#
#    space = creel.spatial_strata.filter(space=stratum[6:8]).first()
#
#    x['creel'] = creel
#    x['mode'] = mode
#    x['season'] = season
#    x['period'] = period
#    x['dtp'] = daytype
#    x['area'] = space
#
    x['stratum'] = stratum

    spc = x.pop('spc')
    species = Species.objects.get(species_code=spc)
    x['species'] = species

    if x.get('date'):
        if x.get('date') == '':
            x['date'] = None
        else:
            my_date = datetime.strptime(x['date'],'%Y-%m-%d')
            my_date = my_date.replace(year=yr)
            x['date'] = my_date


#    x['run'] = int_or_none(x['run'])
    x['rec_tp'] = int_or_none(x['rec_tp'])
    x['sek'] = bool_or_none(x['sek'])
    x['angler1_s'] = int_or_none(x['angler1_s'])
    x['catea1_xy'] = float_or_none(x['catea1_xy'])
    x['catea_xy'] = float_or_none(x['catea_xy'])
    x['catep1_xy'] = float_or_none(x['catep1_xy'])
    x['catep_xy'] = float_or_none(x['catep_xy'])
    x['cater1_xy'] = float_or_none(x['cater1_xy'])
    x['cater_xy'] = float_or_none(x['cater_xy'])
    x['catne'] = float_or_none(x['catne'])
    x['catne1'] = float_or_none(x['catne1'])
    x['catne1_pc'] = float_or_none(x['catne1_pc'])
    x['catne1_se'] = float_or_none(x['catne1_se'])
    x['catne1_vr'] = float_or_none(x['catne1_vr'])
    x['catne_se'] = float_or_none(x['catne_se'])
    x['catne_vr'] = float_or_none(x['catne_vr'])
    x['catno1_s'] = int_or_none(x['catno1_s'])
    x['catno1_ss'] = int_or_none(x['catno1_ss'])
    x['catno_s'] = int_or_none(x['catno_s'])
    x['catno_ss'] = int_or_none(x['catno_ss'])
    x['cif1_nn'] = int_or_none(x['cif1_nn'])
    x['cuenae'] = float_or_none(x['cuenae'])
    x['cuenae1'] = float_or_none(x['cuenae1'])
    x['cuenao'] = float_or_none(x['cuenao'])
    x['cuenao1'] = float_or_none(x['cuenao1'])
    x['effae1'] = float_or_none(x['effae1'])
    x['effae1_pc'] = float_or_none(x['effae1_pc'])
    x['effae1_se'] = float_or_none(x['effae1_se'])
    x['effae1_vr'] = float_or_none(x['effae1_vr'])
    x['effao1_s'] = float_or_none(x['effao1_s'])
    x['effao1_ss'] = float_or_none(x['effao1_ss'])
    x['effpe1'] = float_or_none(x['effpe1'])
    x['effpe1_se'] = float_or_none(x['effpe1_se'])
    x['effpe1_vr'] = float_or_none(x['effpe1_vr'])
    x['effpo1_s'] = float_or_none(x['effpo1_s'])
    x['effpo1_ss'] = float_or_none(x['effpo1_ss'])
    x['effre1'] = float_or_none(x['effre1'])
    x['effre1_se'] = float_or_none(x['effre1_se'])
    x['effre1_vr'] = float_or_none(x['effre1_vr'])
    x['effro1_s'] = float_or_none(x['effro1_s'])
    x['effro1_ss'] = float_or_none(x['effro1_ss'])
    x['hvscat_pc'] = float_or_none(x['hvscat_pc'])
    x['hvsea1_xy'] = float_or_none(x['hvsea1_xy'])
    x['hvsea_xy'] = float_or_none(x['hvsea_xy'])
    x['hvsep1_xy'] = float_or_none(x['hvsep1_xy'])
    x['hvsep_xy'] = float_or_none(x['hvsep_xy'])
    x['hvser1_xy'] = float_or_none(x['hvser1_xy'])
    x['hvser_xy'] = float_or_none(x['hvser_xy'])
    x['hvsne'] = float_or_none(x['hvsne'])
    x['hvsne1'] = float_or_none(x['hvsne1'])
    x['hvsne1_se'] = float_or_none(x['hvsne1_se'])
    x['hvsne1_vr'] = float_or_none(x['hvsne1_vr'])
    x['hvsne_se'] = float_or_none(x['hvsne_se'])
    x['hvsne_vr'] = float_or_none(x['hvsne_vr'])
    x['hvsno1_s'] = int_or_none(x['hvsno1_s'])
    x['hvsno1_ss'] = int_or_none(x['hvsno1_ss'])
    x['hvsno_s'] = int_or_none(x['hvsno_s'])
    x['hvsno_ss'] = int_or_none(x['hvsno_ss'])
    x['mescnt_s'] = int_or_none(x['mescnt_s'])
    x['meswt_s'] = float_or_none(x['meswt_s'])
    x['rod1_s'] = int_or_none(x['rod1_s'])

    item = FR714(**x)
    objects.append(item)

FR714.objects.bulk_create(objects)
print("Done adding FR714 records.")

conn.commit()

#clean up
cur.close()
conn.close()
