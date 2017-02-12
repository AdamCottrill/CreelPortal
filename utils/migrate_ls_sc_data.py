'''
=============================================================
 /home/adam/Documents/djcode/creel_portal/utils/migrate_ls_sc_data.py
 Created: 11 Feb 2017 15:40:28


 DESCRIPTION:



 A. Cottrill
=============================================================
'''

import django
django.setup()

import django_settings
import sqlite3

from creel_portal.models import *

SRC_DB = '/home/adam/Documents/work/Superior/SC_master.db'
conn = sqlite3.connect(SRC_DB)
cursor = conn.cursor()

#==================================
#    FN011  - Project Details

sql = """select PRJ_CD, ARU, COMMENT0, FOF_LOC, FOF_NM, PRJ_DATE0,
         PRJ_DATE1, PRJ_HIS, PRJ_LDR, PRJ_NM, PRJ_SIZE, PRJ_VER,
         V0, WBY WBY_NM from fn011;""" cursor.execute(sql)

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
    x['prj_cd'] = prj_cd_shouldbe(x['prj_cd'])
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
    prj_cd = prj_cd_shouldbe(x.pop('prj_cd'))
    x['creel'] = FN011.objects.get(prj_cd=prj_cd)

    item = FN022(**x)
    objects.append(item)
    #item.save()

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
    prj_cd = prj_cd_shouldbe(prj_cd)
    ssn = x.pop('ssn')
    season = FN022.objects.filter(creel__prj_cd=prj_cd,
                               ssn=ssn).get()
    x['season'] = season
    item = FN023(**x)
    #item.save()
    objects.append(item)
FN023.objects.bulk_create(objects)

# a total hack to accomodate an exception date that
# occurs after the last date of the creel (was May 18th)
x = FN022.objects.filter(creel__prj_cd='NPW_SC12_BSR').get()
x.ssn_date1 = datetime(2012, 5, 21)
x.save()

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
    prj_cd = prj_cd_shouldbe(x.pop('prj_cd'))
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
    prj_cd = prj_cd_shouldbe(x.pop('prj_cd'))
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
    prj_cd = prj_cd_shouldbe(x.pop('prj_cd'))
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
    prj_cd = prj_cd_shouldbe(x.pop('prj_cd'))
    x['creel'] = FN011.objects.get(prj_cd=prj_cd)
    atyunit = int_or_none(x['atyunit'])
    itvunit = int_or_none(x['itvunit'])
    chkflag = int_or_none(x['chkflag'])
    item = FN028(**x)
    #item.save()
    objects.append(item)
FN028.objects.bulk_create(objects)
print("Done adding FN028 records.")

# the mode code used in the FN111 table for the Nipigon creel was 1
# (not S1 as in the fn028 table). Update the FN028 table for now so
# that remaining joins work.)

nip = FN028.objects.filter(creel__prj_cd='LSM_SC03_NIP', mode='S1').get()
nip.mode='1'
nip.save()


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
    prj_cd = prj_cd_shouldbe(x.pop('prj_cd'))
    yr = datetime.strptime(prj_cd[6:8],'%y').year
    my_date = datetime.strptime(x['date'],'%Y-%m-%d')
    my_date = my_date.replace(year=yr)
    x['date'] = my_date
    x['samtm0'] = datetime.strptime(x['samtm0'],'%H:%M')
    creel = FN011.objects.get(prj_cd=prj_cd)
    x['creel'] = creel
    mode_code = x['mode']
    mode = FN028.objects.get(creel=creel, mode=mode_code)
    x['mode'] = mode
    area_code = x['area']
    area = FN026.objects.get(creel=creel, area_lst=area_code)
    x['area'] = area
    item = FN111(**x)
    #item.save()
    objects.append(item)
FN111.objects.bulk_create(objects)
print("Done adding FN111 records.")



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
    prj_cd = prj_cd_shouldbe(x.pop('prj_cd'))
    yr = datetime.strptime(prj_cd[6:8],'%y').year
    my_date = datetime.strptime(x['date'],'%Y-%m-%d')
    my_date = my_date.replace(year=yr)

    creel = FN011.objects.get(prj_cd=prj_cd)
    sama = FN111.objects.get(creel=creel, sama=x['sama'])
    mode_code = x['mode']
    mode = FN028.objects.get(creel=creel, mode=mode_code)
    area_code = x['area']
    area = FN026.objects.get(creel=creel, area_lst=area_code)

    #related objects
    x['creel'] = creel
    x['sama'] = sama
    x['mode'] = mode
    x['area'] = area

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
    prj_cd = prj_cd_shouldbe(prj_cd)

    interview = FN121.objects.get(creel__prj_cd=prj_cd, sam=sam)
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


#==================================
#    FN125  - Bio-Samples


sql = """select prj_cd, sam, spc, grp, fish, flen, tlen, rwt, sex,
         gon, mat, age, agest, clipc, fate from fn125 order by
         prj_cd, sam, spc, grp, fish"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    sam = x.pop('sam')
    spc = x.pop('spc')
    prj_cd = prj_cd_shouldbe(prj_cd)

    catch = FN123.objects.get(interview__creel__prj_cd=prj_cd,
                              interview__sam=sam,
                              species__species_code=spc)
    #related objects
    x['catch'] = catch

    x['flen'] = int_or_none(x['flen'])
    x['tlen'] = int_or_none(x['tlen'])
    x['rwt'] = int_or_none(x['rwt'])
    x['sex'] = int_or_none(x['sex'])
    x['gon'] = int_or_none(x['gon'])
    x['mat'] = int_or_none(x['mat'])
    x['age'] = int_or_none(x['age'])

    item = FN125(**x)
    #item.save()
    objects.append(item)

FN125.objects.bulk_create(objects)
print("Done adding FN125 records.")



#==================================
#    FN127  - Age Estimates


sql = """select prj_cd, sam, spc, grp, fish, ageid,
         agea, agemt, conf, edge, nca from fn127
         order by prj_cd, sam, spc, grp, fish, ageid;"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:

    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    sam = x.pop('sam')
    spc = x.pop('spc')
    grp = x.pop('grp')
    fish = x.pop('fish')
    prj_cd = prj_cd_shouldbe(prj_cd)

    fish = FN125.objects.get(catch__interview__creel__prj_cd=prj_cd,
                              catch__interview__sam=sam,
                              catch__species__species_code=spc,
                             fish=fish, grp=grp)

    x['fish'] = fish
    x['ageid'] = int_or_none(x['ageid'])
    x['agea'] = int_or_none(x['agea'])
    x['conf'] = int_or_none(x['conf'])
    x['nca'] = int_or_none(x['nca'])

    item = FN127(**x)
    objects.append(item)

FN127.objects.bulk_create(objects)
print("Done adding FN127 records.")



#==================================
#    FR713  - Effort Estimates


sql = """ select prj_cd, strat, [date], angler_s, angler_ss, atycnt_s,
          aty_days, aty_nn, chkcnt_s, cif_nn, itvcnt_s, person_s,
          rod_s, rod_ss, tripno, [run], rec_tp from fr713
          order by prj_cd, strat;
"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k:v for k,v in zip(col_names, record)}
    prj_cd = x.pop('prj_cd')
    prj_cd = prj_cd_shouldbe(prj_cd)
    yr = datetime.strptime(prj_cd[6:8],'%y').year

    stratum = x.get('strat')

    creel = FN011.objects.get(prj_cd=prj_cd)
    #get all of the related objects:
    mode = creel.modes.filter(mode=stratum[9:]).first()
    season = creel.seasons.filter(ssn=stratum[:2]).first()
    if season:
        daytype = season.daytypes.filter(dtp=stratum[3]).first()
    else:
        daytype = None
    if daytype:
        period = daytype.periods.filter(prd=stratum[4]).first()
    else:
        period = None

    space = creel.spatial_strata.filter(space=stratum[6:8]).first()

    x['creel'] = creel
    x['mode'] = mode
    x['season'] = season
    x['period'] = period
    x['dtp'] = daytype
    x['area'] = space

    if x.get('date'):
        if x.get('date') == '':
            x['date'] = None
        else:
            my_date = datetime.strptime(x['date'],'%Y-%m-%d')
            my_date = my_date.replace(year=yr)
            x['date'] = my_date

    x['angler_s'] = int_or_none(x['angler_s'])
    x['angler_ss']= int_or_none(x['angler_ss'])
    x['atycnt_s']= int_or_none(x['atycnt_s'])
    x['aty_days']= int_or_none(x['aty_days'])
    x['aty_nn']= int_or_none(x['aty_nn'])
    x['chkcnt_s']= int_or_none(x['chkcnt_s'])
    x['cif_nn']= int_or_none(x['cif_nn'])
    x['itvcnt_s']= int_or_none(x['itvcnt_s'])
    x['person_s']= int_or_none(x['person_s'])
    x['rod_s']= int_or_none(x['rod_s'])
    x['rod_ss']= int_or_none(x['rod_ss'])
    x['tripno']= int_or_none(x['tripno'])
    x['run']= int_or_none(x['run'])
    x['rec_tp']= int_or_none(x['rec_tp'])


    item = FR713(**x)
    objects.append(item)

FR713.objects.bulk_create(objects)
print("Done adding FR713 records.")



#==================================
#    FR714  - Catch Estimates


sql = """select prj_cd, strat, spc, sek, [date], rod1_s, angler1_s,
         catno1_s, catno1_ss, catno_s, catno_ss, cif1_nn, hvsno1_s,
         hvsno1_ss, hvsno_s, hvsno_ss, mescnt_s, rec_tp, [run] from fr714
         order by prj_cd, strat, spc, sek;"""

cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k:v for k,v in zip(col_names, record)}

    prj_cd = x.pop('prj_cd')
    prj_cd = prj_cd_shouldbe(prj_cd)
    yr = datetime.strptime(prj_cd[6:8],'%y').year

    stratum = x.get('strat')

    creel = FN011.objects.get(prj_cd=prj_cd)

    spc = x.pop('spc')
    species = Species.objects.get(species_code=spc)

    mode = creel.modes.filter(mode=stratum[9:]).first()
    season = creel.seasons.filter(ssn=stratum[:2]).first()
    if season:
        daytype = season.daytypes.filter(dtp=stratum[3]).first()
    else:
        daytype = None
    if daytype:
        period = daytype.periods.filter(prd=stratum[4]).first()
    else:
        period = None

    space = creel.spatial_strata.filter(space=stratum[6:8]).first()

    x['creel'] = creel
    x['mode'] = mode
    x['season'] = season
    x['period'] = period
    x['dtp'] = daytype
    x['area'] = space
    x['species'] = species

    if x.get('date'):
        if x.get('date') == '':
            x['date'] = None
        else:
            my_date = datetime.strptime(x['date'],'%Y-%m-%d')
            my_date = my_date.replace(year=yr)
            x['date'] = my_date

    x['sek'] = bool_or_none(x['sek'])
    x['rod1_s'] = int_or_none(x['rod1_s'])
    x['angler1_s'] = int_or_none(x['angler1_s'])
    x['catno1_s'] = int_or_none(x['catno1_s'])
    x['catno1_ss'] = int_or_none(x['catno1_ss'])
    x['catno_s'] = int_or_none(x['catno_s'])
    x['catno_ss'] = int_or_none(x['catno_ss'])
    x['cif1_nn'] = int_or_none(x['cif1_nn'])
    x['hvsno1_s'] = int_or_none(x['hvsno1_s'])
    x['hvsno1_ss'] = int_or_none(x['hvsno1_ss'])
    x['hvsno_s'] = int_or_none(x['hvsno_s'])
    x['hvsno_ss'] = int_or_none(x['hvsno_ss'])
    x['mescnt_s'] = int_or_none(x['mescnt_s'])
    x['rec_tp'] = int_or_none(x['rec_tp'])
    x['run'] = int_or_none(x['run'])

    item = FR714(**x)
    objects.append(item)

FR714.objects.bulk_create(objects)
print("Done adding FR714 records.")

#clean up
cur.close()
conn.close()
