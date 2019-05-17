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
from django.utils.functional import cached_property

from . import utils

logger = logging.getLogger(__name__)


class Task(celery.Task):
    @cached_property
    def task(self):
        if not hasattr(self, '_task') or self._task is None:
            from . import models
            if self.request.id is None:
                task_id = uuid.uuid4().hex
            else:
                task_id = self.request.id
            self._task, _ = models.CeleryTask.objects.get_or_create(task_id=task_id)
        return self._task

    def apply_async(self, args=None, kwargs=None, *args_, **kwargs_):
        from . import models
        user = kwargs_.get('user')
        if user is None:
            user = utils.get_user()
        task_id = kwargs_.pop('task_id', None)
        if task_id is None:
            task_id = uuid.uuid4().hex
        models.CeleryTask.objects.create(
            user=user, task_id=task_id, task_path=self.name,
            args=yaml.dump(args if args is not None else ()),
            kwargs=yaml.dump(kwargs if kwargs is not None else {}))
        result = super(Task, self).apply_async(args=args, kwargs=kwargs, task_id=task_id, *args_, **kwargs_)
        logger.debug('created celery task : %s %s name=%s', user, result.task_id, self.name)
        return result

    def __call__(self, *args, **kwargs):
        self._task = None
        logger.debug("%s %s is started.", self.request.id, self.task)
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
            retval = self.run(*args, **kwargs)
            return self.handle_retval(retval)
        except SystemExit:
            raise  # no log in revoke
        except:
            if self.task.status == 'started':
                self.task.status = 'failed'
            logger.exception('celery task failed')
            raise
        finally:
            if self.task.status == 'started':
                self.task.status = 'succeeded'
            self.task.end_at = timezone.now()
            self.task.save()
            utils.reset_task()
            logger.debug("%s is terminated.", self.request.id)

    def on_success(self, retval, task_id, args, kwargs):
        if (self.task.status == 'revoked' or self.task.status == 'cancelled' or
                self.task.status == 'retry_rejected'):
            return
        self.task.status = 'succeeded'
        self.task.save()
        logger.debug("%s is on success.", self.request.id)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        self.task.status = 'retried'
        self.task.stack_trace = str(einfo)
        self.task.save()
        logger.debug("%s is on retry. %s", self.request.id, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.task.status = 'failed'
        self.task.stack_trace = str(einfo)
        self.task.save()
        logger.debug("%s is on failure. %s", self.request.id, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self.task.status == 'succeeded':
            self.task.result_text = json.dumps(retval)
            self.task.save()
        logger.debug("%s after_return status=%s.", self.request.id, status)

    def handle_retval(self, retval):
        return retval


class FileTask_(Task):

    def handle_retval(self, retval):
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
                return retval
            return filename
        except:
            logger.exception('FileTask_ failed')
            raise


def FileTask(extension, base_class=FileTask_):
    name = extension[0].upper() + extension[1].lower()
    return type('{}FileTask'.format(name), (base_class, ), {'ext': extension})
