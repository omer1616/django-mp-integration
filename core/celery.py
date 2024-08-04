from __future__ import absolute_import, unicode_literals
from .celery_schedule_conf import CELERY_BEAT_SCHEDULE
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = CELERY_BEAT_SCHEDULE