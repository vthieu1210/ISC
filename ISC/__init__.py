from __future__ import absolute_import
import sys
sys.dont_write_bytecode = True
from .celery import app as celery_app
