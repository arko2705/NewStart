
from newstartapp.models import Num,QueryStartStat

def model_update(companynumber,stat):
    Num(companynumber=companynumber).save()
    QueryStartStat(stat=stat).save()