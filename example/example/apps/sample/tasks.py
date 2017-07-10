# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import logging
from celery.schedules import crontab
from heavy_celery import base
from example.celery_conf import app
from heavy_celery.cron import spawner as _cron_scheduler

logger = logging.getLogger(__name__)


@app.task(base=base.Task)
def hello_world(*args, **kwargs):
    logger.info("test task {} {}".format(args, kwargs))
    return 'hello world'


@app.task(base=base.Task)
def test_exception(*args, **kwargs):
    raise Exception('hello world')


@app.task()
def cron_scheduler():
    _cron_scheduler()


app.conf.beat_schedule = {
    'cron_scheduler': {
        'task': 'example.apps.sample.tasks.cron_scheduler',
        'schedule': crontab(),
        'args': (),
        'options': dict(queue='time_sensitive', routing_key='time_sensitive_tasks'),
    },
}
