# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import logging

from django.db.models import Q, F
from . import models, utils

logger = logging.getLogger(__name__)


def spawner():
    '''
    from <project_name>.apps.heavy_celery.cron import spawner as _cron_scheduler
    @app.task()
    def cron_scheduler():
        _cron_scheduler()


    app.conf.beat_schedule = {
        'cron_scheduler': {
            'task': '<project_name>.apps.common.tasks.cron_scheduler',
            'schedule': crontab(),
            'args': (),
            'options': dict(queue='time_sensitive', routing_key='time_sensitive_tasks'),
        },
    }
    '''
    now = utils.get_now()
    logger.debug('cron spawner {}'.format(now))
    for schedule in models.CronSchedule.objects.filter(
            Q(next_time__lte=now),
            Q(total_run_count__lt=F('max_run_count')) | Q(max_run_count=-1),
            Q(expires__gt=now) | Q(expires__isnull=True)).select_related('task'):
        logger.debug('cron spawner {} {} run start'.format(now, schedule))
        try:
            schedule.run(now)
        except:
            logger.exception('{} failed'.format(schedule))
        logger.debug('cron spawner {} {} run end'.format(now, schedule))
