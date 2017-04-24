
from creel_portal.models import *


creel = FN011.sa.query().first()
print(creel)

season = FN022.sa.query().first()
print(season)


# create a queryset that contains calculate the number of interviews in each
# samlog

prj_cd = 'LHA_SC06_122'
foo = FN111.sa.query().join(FN011.sa.interview_logs).\
      filter(FN011.sa.prj_cd==prj_cd).all()
print(foo[0])

for x in foo[:10]:
    print(str(x))
