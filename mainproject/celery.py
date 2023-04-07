from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainproject.settings')
app = Celery('mainproject')

app.conf.enable_utc=False
app.conf.update(timezone = 'Asia/Kathmandu')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


task = app.task


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))