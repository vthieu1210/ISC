from ISCSM.models import *

def getZone(request):
    listzone = Zone.objects.all()
    return { 'listzone' : listzone }
