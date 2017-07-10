# coding: utf-8
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

app = Celery("example")

CELERY_TIMEZONE = 'Asia/Tokyo'

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
