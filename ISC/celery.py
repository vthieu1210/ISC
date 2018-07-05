from __future__ import absolute_import, unicode_literals
import os, sys
from celery import Celery
from celery.schedules import *

sys.dont_write_bytecode = True

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ISC.settings')

app = Celery('ISC')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'scan_Web_Service': {
    #    'task': 'ISCSM.tasks.scanWebService',
    #    'schedule': crontab(hour=19,minute=0),
    # },
    # 'scan_Win_Service': {
    #    'task': 'ISCSM.tasks.scanWinService',
    #    'schedule': crontab(hour=19,minute=0),
    # },
}
