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

os.chdir('/home/adam/Documents/djcode/creel_portal')
django.setup()


import django_settings
import sqlite3
from datetime import datetime

from creel_portal.models import *

from utils.helper_fcts import *


def clear_fr714(trg_db):
    """

    Arguments:
    - `trg_db`:
    """
    import sqlite3

    conn = sqlite3.connect(trg_db)
    cursor = conn.cursor()
    sql = """DELETE FROM creel_portal_fr714
      WHERE creel_id IN (
    SELECT fn011.id
      FROM creel_portal_fn011 fn011
           JOIN
           creel_portal_lake lake ON lake.id = fn011.lake_id
     WHERE lake.abbrev = 'HU');
    """
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("FR714 records cleared.")



#SRC_DB = '/home/adam/Documents/work/Superior/SC_master.db'
#SRC_DB = '/home/adam/Documents/work/Superior/lhmu_sc_warehouse.db'
SRC_DB = "C:/1work/ScrapBook/lhmu_sc_warehouse.db"

conn = sqlite3.connect(SRC_DB)
cursor = conn.cursor()

#lake = Lake(lake_name='Huron', abbrev='HU')
#lake.save()


x = FN011.objects.all().values_list('prj_cd','id')
prj_cd_map = {k:v for k,v in x}

x = Species.objects.all().values_list('species_code','id')
species_map = {k:v for k,v in x}


#x = FN022.objects.all().values_list('creel__prj_cd', 'ssn','id')
#season_map = {k:v for k,v in x}



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


trg_db = "C:/1work/Python/djcode/creel_portal/db/db.sqlite3"
clear_fr714(trg_db)

START = datetime.now()
cursor.execute(sql)
rs = cursor.fetchall()
col_names = [x[0].lower() for x in cursor.description]
objects = []

for record in rs:
    x = {k:v for k,v in zip(col_names, record)}

    prj_cd = x.pop('prj_cd')
    yr = datetime.strptime(prj_cd[6:8],'%y').year

    stratum = x.get('strat')

    #creel = FN011.objects.get(prj_cd=prj_cd)
    creel_id = prj_cd_map.get(prj_cd)

    spc = x.pop('spc')
    #species = Species.objects.get(species_code=spc)
    species_id = species_map.get(int(spc))

    mode_code = stratum[9:]
    if mode_code == "++":
        mode = None
    else:
        try:
            #mode = creel.modes.filter(mode=mode_code).get()
            mode = FN028.objects.filter(mode=mode_code,
                                        creel_id=creel_id).get()
        except:
            print("Problem with {} - {} {} ".format("Mode", prj_cd, stratum))
            next

    #space = creel.spatial_strata.filter(space=stratum[6:8]).first()
    space_code = stratum[6:8]
    if space_code == "++":
        space = None
    else:
        try:
            #space = creel.spatial_strata.filter(space=space_code).get()
            space = FN026.objects.filter(space=space_code,
                                         creel_id=creel_id).get()
        except:
            print("Problem with {} - {} {} ".format("Space", prj_cd, stratum))
            next

    #season = creel.seasons.filter(ssn=stratum[:2]).first()
    season_code = stratum[:2]
    if season_code == "++":
        season = None
    else:
        try:
            #season = creel.seasons.filter(ssn=season_code).get()
            season = FN022.objects.filter(ssn=season_code,
                                          creel_id=creel_id).get()
        except:
            print("Problem with {} - {} {} ".format("Season", prj_cd, stratum))
            next

    if season:
        daytype_code = stratum[3]
        if daytype_code == "+":
            daytype = None
        else:
            try:
                daytype = season.daytypes.filter(dtp=daytype_code).get()
            except:
                print("Problem with {} - {} {} ".format("Daytype", prj_cd,
                                                        stratum))
                next
    else:
        daytype = None

    if daytype:
        period_code = stratum[4]
        if period_code == "+":
            period = None
        else:
            try:
                period = daytype.periods.filter(prd=period_code).get()
            except:
                print("Problem with {} - {} {} ".format("Period", prj_cd,
                                                        stratum))
                next
    else:
        period = None

    #x['creel'] = creel
    #x['species'] = species
    x['creel_id'] = creel_id
    x['species_id'] = species_id
    x['area'] = space
    x['mode'] = mode
    x['season'] = season
    x['period'] = period
    x['dtp'] = daytype

    if x.get('date'):
        if x.get('date') == '':
            x['date'] = None
        else:
            my_date = datetime.strptime(x['date'],'%Y-%m-%d')
            my_date = my_date.replace(year=yr)
            x['date'] = my_date

    x['run'] = int_or_none(x['run'])
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

PROCESSED = datetime.now()

FR714.objects.bulk_create(objects)
print("Done adding FR714 records.")


COMPLETE = datetime.now()

print("Elapsed Time = "+ str(COMPLETE - START).split('.')[0])
print("Processing Time = "+ str(PROCESSED - START).split('.')[0])
print("Insert Time = "+ str(COMPLETE - PROCESSED).split('.')[0])

# Elapsed Time = 0:05:15 - ORM - ignore errors
# Elapsed Time = 0:04:43 - ORM with try-catch
# Elapsed Time = 0:03:27 using project and spc maps
