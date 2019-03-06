# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

# import datetime
# import logging

# # Task Signals
# from celery.signals import before_task_publish
# from celery.signals import after_task_publish
# from celery.signals import task_prerun
# from celery.signals import task_postrun
# from celery.signals import task_retry
# from celery.signals import task_success
# from celery.signals import task_failure
# from celery.signals import task_revoked
# from celery.signals import task_unknown
# from celery.signals import task_rejected

# # App Signals
# from celery.signals import import_modules

# # Worker Signals
# from celery.signals import celeryd_after_setup
# from celery.signals import celeryd_init
# from celery.signals import worker_init
# from celery.signals import worker_ready
# from celery.signals import heartbeat_sent
# from celery.signals import worker_process_init
# from celery.signals import worker_process_shutdown
# from celery.signals import worker_shutdown

# # Beat Signals
# from celery.signals import beat_init
# from celery.signals import beat_embedded_init

# # Eventlet Signals
# from celery.signals import eventlet_pool_started
# from celery.signals import eventlet_pool_preshutdown
# from celery.signals import eventlet_pool_postshutdown
# from celery.signals import eventlet_pool_apply

# # Logging Signals
# from celery.signals import setup_logging
# from celery.signals import after_setup_logger
# from celery.signals import after_setup_task_logger

# # Command signals
# from celery.signals import user_preload_options

# Deprecated Signals
# from celery.signals import task_sent
# from django.utils import timezone

# from . import models, utils


# logger = logging.getLogger(__name__)


# @before_task_publish.connect
# def before_task_publish_handler(*args, **kwargs):
#     logger.debug('Task Signals before_task_publish {} {}'.format(args, kwargs))


# @after_task_publish.connect
# def after_task_publish_handler(*args, **kwargs):
#     logger.debug('Task Signals after_task_publish {} {}'.format(args, kwargs))


# @task_prerun.connect
# def task_prerun_handler(*args, **kwargs):
#     logger.debug('Task Signals task_prerun {} {}'.format(args, kwargs))


# @task_postrun.connect
# def task_postrun_handler(*args, **kwargs):
#     logger.debug('Task Signals task_postrun {} {}'.format(args, kwargs))


# @task_retry.connect
# def task_retry_handler(*args, **kwargs):
#     logger.debug('Task Signals task_retry {} {}'.format(args, kwargs))


# @task_success.connect
# def task_success_handler(*args, **kwargs):
#     logger.debug('Task Signals task_success {} {}'.format(args, kwargs))


# @task_failure.connect
# def task_failure_handler(*args, **kwargs):
#     logger.debug('Task Signals task_failure {} {}'.format(args, kwargs))


# @task_revoked.connect
# def task_revoked_handler(request=None, *args, **kwargs):
#     try:
#         task = models.CeleryTask.objects.get(task_id=request.id)
#         task.status = 'revoked'
#         task.save()
#     except models.CeleryTask.DoesNotExist:
#         pass
#     logger.debug('Task Signals task_revoked {} {}'.format(args, kwargs))
#     utils.reset_task()


# @task_unknown.connect
# def task_unknown_handler(*args, **kwargs):
#     logger.debug('Task Signals task_unknown {} {}'.format(args, kwargs))


# @task_rejected.connect
# def task_rejected_handler(*args, **kwargs):
#     logger.debug('Task Signals task_rejected {} {}'.format(args, kwargs))


# @import_modules.connect
# def import_modules_handler(*args, **kwargs):
#     logger.debug('App Signals import_modules {} {}'.format(args, kwargs))


# @celeryd_after_setup.connect
# def celeryd_after_setup_handler(*args, **kwargs):
#     logger.debug('Worker Signals celeryd_after_setup {} {}'.format(args, kwargs))


# @celeryd_init.connect
# def celeryd_init_handler(*args, **kwargs):
#     logger.debug('Worker Signals celeryd_init {} {}'.format(args, kwargs))


# @worker_init.connect
# def worker_init_handler(*args, **kwargs):
#     logger.debug('Worker Signals worker_init {} {}'.format(args, kwargs))


# @worker_ready.connect
# def worker_ready_handler(*args, **kwargs):
#     logger.debug('Worker Signals worker_ready {} {}'.format(args, kwargs))


# @heartbeat_sent.connect
# def heartbeat_sent_handler(*args, **kwargs):
#     # logger.debug('Worker Signals heartbeat_sent {} {}'.format(args, kwargs))
#     whb, _ = models.WorkerHeartBeat.objects.get_or_create(worker_id=utils.get_worker_id())
#     whb.updated_at = timezone.now()
#     whb.save(update_fields=['updated_at'])
#     # models.Worker.objects.update_or_create(
#     #     worker_id=_get_worker_id(), defaults=dict(beated_at=timezone.now()))
#     # timeout = timezone.now() - datetime.timedelta(minutes=10)
#     # models.Worker.objects.filter(beated_at__lt=timeout).update(status=models.Worker.State.BEAT_FAILED)


# @worker_process_init.connect
# def worker_process_init_handler(*args, **kwargs):
#     logger.debug('Worker Signals worker_process_init {} {}'.format(args, kwargs))
#     # models.Worker.objects.get_or_create(worker_id=_get_worker_id())


# @worker_process_shutdown.connect
# def worker_process_shutdown_handler(*args, **kwargs):
#     # worker, _ = models.Worker.objects.get_or_create(worker_id=_get_worker_id())
#     # worker.ended_at = timezone.now()
#     # worker.status = models.Worker.State.STOPPED
#     # worker.save()

#     logger.debug('Worker Signals worker_process_shutdown {} {}'.format(args, kwargs))
#     # with open('/data/static/django-celery.log', 'a') as fp:
#     #     fp.writer('Worker Signals worker_process_shutdown {} {}\n'.format(args, kwargs))


# @worker_shutdown.connect
# def worker_shutdown_handler(*args, **kwargs):
#     logger.debug('Worker Signals worker_shutdown {} {}'.format(args, kwargs))
#     # with open('/data/static/django-celery2.log', 'a') as fp:
#     #     fp.writer('Worker Signals worker_shutdown {} {}\n'.format(args, kwargs))


# @beat_init.connect
# def beat_init_handler(*args, **kwargs):
#     logger.debug('Beat Signals beat_init {} {}'.format(args, kwargs))


# @beat_embedded_init.connect
# def beat_embedded_init_handler(*args, **kwargs):
#     logger.debug('Beat Signals beat_embedded_init {} {}'.format(args, kwargs))


# @eventlet_pool_started.connect
# def eventlet_pool_started_handler(*args, **kwargs):
#     logger.debug('Eventlet Signals eventlet_pool_started {} {}'.format(args, kwargs))


# @eventlet_pool_preshutdown.connect
# def eventlet_pool_preshutdown_handler(*args, **kwargs):
#     logger.debug('Eventlet Signals eventlet_pool_preshutdown {} {}'.format(args, kwargs))


# @eventlet_pool_postshutdown.connect
# def eventlet_pool_postshutdown_handler(*args, **kwargs):
#     logger.debug('Eventlet Signals eventlet_pool_postshutdown {} {}'.format(args, kwargs))


# @eventlet_pool_apply.connect
# def eventlet_pool_apply_handler(*args, **kwargs):
#     logger.debug('Eventlet Signals eventlet_pool_apply {} {}'.format(args, kwargs))


# @setup_logging.connect
# def setup_logging_handler(*args, **kwargs):
#     logger.debug('Logging Signals setup_logging {} {}'.format(args, kwargs))


# @after_setup_logger.connect
# def after_setup_logger_handler(*args, **kwargs):
#     logger.debug('Logging Signals after_setup_logger {} {}'.format(args, kwargs))


# @after_setup_task_logger.connect
# def after_setup_task_logger_handler(*args, **kwargs):
#     logger.debug('Logging Signals after_setup_task_logger {} {}'.format(args, kwargs))


# @user_preload_options.connect
# def user_preload_options_handler(*args, **kwargs):
#     logger.debug('Command signals user_preload_options {} {}'.format(args, kwargs))


# @task_sent.connect
# def task_sent_handler(*args, **kwargs):
#     logger.debug('Deprecated Signals task_sent {} {}'.format(args, kwargs))
