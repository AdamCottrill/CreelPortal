'''=============================================================
 /home/adam/Documents/djcode/creel_portal/utils/common_objects.py
 Created: 12 Feb 2017 13:53:44


 DESCRIPTION:

  a little script to help load model objects for common entities (Lake
  and Species so far)

 A. Cottrill
=============================================================

'''


import django
django.setup()

import csv
import django_settings

from creel_portal.models import *


lake = Lake(lake_name='Huron', abbrev='HU')
lake.save()
lake = Lake(lake_name='Superior', abbrev='SU')
lake.save()

#  HOME
csv_file = '/home/adam/Documents/work/Species_CodeTable.txt'
#  WORK
csv_file = 'C:/1work/scrapbook/Species_CodeTable.txt'
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    spc_list = list(reader)




objects = []
for spc in spc_list:
    species = Species(species_code=spc[0], common_name=spc[1],
                      scientific_name=spc[2])
    objects.append(species)

Species.objects.bulk_create(objects)
print("Done adding Species.")
