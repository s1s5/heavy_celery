# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import uuid
import logging
import celery
import json
import yaml
import six

from django.core.files import File
from django.core.files.base import ContentFile
from django.utils import timezone

from . import models, utils

logger = logging.getLogger(__name__)


class Task(celery.Task):
    @property
    def task(self):
        if not hasattr(self, '_task') or self._task is None:
            if self.request.id is None:
                task_id = uuid.uuid4().hex
            else:
                task_id = self.request.id
            self._task, _ = models.CeleryTask.objects.get_or_create(task_id=task_id)
        return self._task

    def apply_async(self, args=None, kwargs=None, *args_, **kwargs_):
        user = kwargs_.get('user')
        if user is None:
            user = utils.get_user()
        result = super(Task, self).apply_async(args=args, kwargs=kwargs, *args_, **kwargs_)
        logger.debug('created celery task : {} {} name={}'.format(user, result.task_id, self.name))
        models.CeleryTask.objects.create(
            user=user, task_id=result.task_id, task_path=self.name,
            args=yaml.dump(args if args is not None else ()),
            kwargs=yaml.dump(kwargs if kwargs is not None else {}))
        return result

    def __call__(self, *args, **kwargs):
        self._task = None
        logger.debug("{} {} is started.".format(self.request.id, self.task))
        try:
            utils.set_task(self.task)
            if self.task.status == 'cancel':
                self.task.status = 'cancelled'
                return
            elif self.task.status != 'sent':
                self.task.status = 'retry_rejected'
                return
            self.task.status = 'started'
            self.task.start_at = timezone.now()
            self.task.save()
            return self.run(*args, **kwargs)
        except SystemExit:
            raise  # no log in revoke
        except:
            logger.exception('celery task failed')
            raise
        finally:
            self.task.end_at = timezone.now()
            self.task.save()
            utils.reset_task()
            logger.debug("{} is terminated.".format(self.request.id))

    def on_success(self, retval, task_id, args, kwargs):
        if (self.task.status == 'revoked' or self.task.status == 'cancelled' or
                self.task.status == 'retry_rejected'):
            return
        self.task.status = 'succeeded'
        self.task.save()
        logger.debug("{} is on success.".format(self.request.id))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        self.task.status = 'retried'
        self.task.stack_trace = str(einfo)
        self.task.save()
        logger.debug("{} is on retry. {}".format(self.request.id, einfo))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.task.status = 'failed'
        self.task.stack_trace = str(einfo)
        self.task.save()
        logger.debug("{} is on failure. {}".format(self.request.id, einfo))

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self.task.status == 'succeeded':
            self.task.result_text = json.dumps(retval)
            self.task.save()
        logger.debug("{} after_return status={}.".format(self.request.id, status))


class FileTask_(Task):

    def __call__(self, *args, **kwargs):
        retval = super(FileTask_, self).__call__(*args, **kwargs)
        try:
            filename = '{}.{}'.format(uuid.uuid4().hex, self.ext)
            if hasattr(retval, 'read'):
                self.task.result_data.save(filename, File(retval), save=True)
            elif isinstance(retval, six.text_type):
                self.task.result_data.save(filename, ContentFile(
                    retval.encode(getattr(self, 'encode', 'UTF-8'))), save=True)
            elif isinstance(retval, six.string_types) or isinstance(retval, six.binary_type):
                self.task.result_data.save(filename, ContentFile(retval), save=True)
            else:
                return None
            self.task.save()
            return filename
        except:
            logger.exception('FileTask_ failed')
            raise


def FileTask(extension, base_class=FileTask_):
    name = extension[0].upper() + extension[1].lower()
    return type('{}FileTask'.format(name), (base_class, ), {'ext': extension})
