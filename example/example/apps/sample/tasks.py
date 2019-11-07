# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import logging
import time
import io

from celery.schedules import crontab
from example.celery_conf import app
from heavy_celery import base, utils
from heavy_celery.cron import spawner as _cron_scheduler

logger = logging.getLogger(__name__)


@app.task(base=base.Task)
def hello_world(*args, **kwargs):
    logger.info("test task {} {}".format(args, kwargs))
    return 'hello world'


@app.task(base=base.Task)
def test_exception(*args, **kwargs):
    raise Exception('hello world')


@app.task(base=base.Task)
def hello_world2(*args, **kwargs):
    logger.info("test task started {} {}".format(args, kwargs))
    time.sleep(50)
    logger.info("test task {} {}".format(args, kwargs))
    time.sleep(50)
    logger.info("test task ended {} {}".format(args, kwargs))
    return 'hello world2'


@app.task(base=base.FileTask("txt"))
def create_file(*args, **kwargs):
    sio = io.StringIO()
    sio.write('args={} kwargs={}'.format(args, kwargs))
    sio.seek(0)
    return sio


@app.task(base=base.FileTask("txt"))
def create_file2(*args, **kwargs):
    return 'args={} kwargs={}'.format(args, kwargs)


@app.task()
def cron_scheduler():
    _cron_scheduler()


@app.task()
def celery_revoke(task_id):
    logger.info("revoking {}".format(task_id))
    from celery.task.control import revoke
    revoke(task_id, terminate=True)
    logger.info("revoked! {}".format(task_id))


app.conf.beat_schedule = {
    'cron_scheduler': {
        'task': 'example.apps.sample.tasks.cron_scheduler',
        'schedule': crontab(),
        'args': (),
        'options': dict(queue='time_sensitive', routing_key='time_sensitive_tasks'),
    },
}
