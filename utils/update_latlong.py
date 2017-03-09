'''=============================================================
c:/1work/Python/djcode/creel_portal/utils/update_latlong.py
Created: 07 Mar 2017 11:48:19


DESCRIPTION:

This script reads in teh lat-lon for creel sites as provided by LCM
and updates the sites in creel_portal so that they can be displayed on
a leaflet map.pyt

A. Cottrill
=============================================================

'''


import csv



import django
django.setup()

import csv
import django_settings

from creel_portal.models import *


SRC = 'c:/1work/ScrapBook/CreelSites_latlong.csv'

pts = []

with open(SRC, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        pts.append(row)



for pt in pts:
    space = FN026.objects.filter(creel__prj_cd=pt[0], space=pt[2]).first()
    lat = pt[5] if pt[5] != "" else None
    lon = pt[6] if pt[6] != "" else None
    if space and lat and lon:
        space.ddlat = lat
        space.ddlon = lon
        space.save()
    else:
        print("Snap! {} - {}".format(pt[0], pt[2]))

print("Done!")

with_pts = FN026.objects.exclude(ddlat__isnull).all()



#SUPERIOR



pts = [['LSM_SC00_BAS', '01', '', '1', 46.852881, -84.407624],
       ['LSM_SC00_BAS', '02', '', '2', 46.913423, -84.462212],
       ['LSM_SC00_BAS', '03', '', '3', 46.919286, -84.567269],
       ['LSM_SC00_BAT', '01', 'BATCHAWANA I', '1', 46.858984, -84.399332],
       ['LSM_SC00_BAT', '02', 'BATCHAWANA II', '2', 46.906849, -84.446047],
       ['LSM_SC00_SPR', 'PA', 'PANCAKE RIVER', 'PA', 46.958438, -84.661245],
       ['LSM_SC00_SPR', 'CH', 'CHIPPEWA RIVER', 'CH', 46.92947, -84.425578],
       ['NPW_SC11_BSR', '10', 'BLACK STURGEON RIVER', '10', 48.83625, -88.40401],
       ['NPW_SC12_BSR', '10', 'BLACK STURGEON RIVER', '1', 48.83625, -88.40401],
       ['NPW_SC12_BSR', '20', 'EVERARD ROAD', '2', 48.898949, -88.362219],
       ['NPW_SC12_BSR', '30', 'DAM', '3', 48.921474, -88.389915],
       ['NPW_SC13_BSR', '10', 'BLACK STURGEON RIVER', '10', 48.83625, -88.40401],
       ['NPW_SC13_BSR', '20', 'EVERARD ROAD', '20', 48.898949, -88.362219],
       ['NPW_SC13_BSR', '30', 'DUMP ROAD', '30', 48.871895, -88.340499]]

for pt in pts:
    space = FN026.objects.filter(creel__prj_cd=pt[0], space=pt[1]).first()
    lat = pt[4] if pt[4] != "" else None
    lon = pt[5] if pt[5] != "" else None
    if space and lat and lon:
        space.ddlat = lat
        space.ddlon = lon
        space.save()
    else:
        print("Snap! {} - {}".format(pt[0], pt[1]))

print("Done!")




foo = FN026.objects.filter(ddlat_isnull=False).all()

for x in foo:
    x.geom={'type': 'Point', 'coordinates': [x.ddlon, x.ddlat]}
    x.save()
