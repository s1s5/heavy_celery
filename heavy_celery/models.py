# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from future.utils import python_2_unicode_compatible
import yaml

from celery.task.control import revoke as celery_revoke

from django.conf import settings
from django.db import models
from django.utils.functional import SimpleLazyObject
from django.utils.module_loading import import_string

from . import utils


TASK_STATE = (
    # from celery.events.state
    ('sent', 'PENDING', ),
    ('received', 'RECEIVED', ),
    ('started', 'STARTED', ),
    ('failed', 'FAILURE', ),
    ('retried', 'RETRY', ),
    ('succeeded', 'SUCCESS', ),
    ('revoked', 'REVOKED', ),
    ('rejected', 'REJECTED', ),

    # custom state
    ('cancel', 'CANCEL'),
    ('cancelled', 'CANCELLED'),
    ('revoking', 'REVOKING'),
    ('retry_rejected', 'RETRY_REJECTED'),
)


@python_2_unicode_compatible
class TaskSignature(models.Model):
    name = models.CharField('名前', max_length=256, blank=True, null=True)
    description = models.TextField('詳細', blank=True, null=True)

    task_path = models.CharField('タスク名', max_length=256)
    args = models.TextField('引数', blank=True, null=True)
    kwargs = models.TextField('kw引数', blank=True, null=True)
    options = models.TextField('タスクオプション', blank=True, null=True)

    def _read_yaml(self, value, default_value):
        if not value:
            return default_value
        return yaml.load(value)

    def get_args(self):
        return self._read_yaml(self.args, ())

    def get_kwargs(self):
        return self._read_yaml(self.kwargs, {})

    def get_options(self):
        return self._read_yaml(self.options, {})

    def run(self):
        import_string(self.task_path).apply_async(
            args=self.get_args(), kwargs=self.get_kwargs(), **self.get_options())

    def save(self, *args, **kwargs):
        if not (isinstance(self.get_args(), (tuple, list)) and
                isinstance(self.get_kwargs(), dict) and
                isinstance(self.get_options(), dict)):
            raise TypeError()
        return super(TaskSignature, self).save(*args, **kwargs)

    def __str__(self):
        return '[{}]{}'.format(self.pk, self.name if self.name else self.task_path)


@python_2_unicode_compatible
class CronSchedule(models.Model):
    name = models.CharField('名前', max_length=256, blank=True, null=True)
    description = models.TextField('詳細', blank=True, null=True)

    cron_expr = models.CharField('cron', max_length=256)
    next_time = models.DateTimeField(blank=True, null=True)
    task = models.ForeignKey(TaskSignature, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField('有効期限', blank=True, null=True)

    last_run_at = models.DateTimeField('最終実行日時', blank=True, null=True)
    total_run_count = models.PositiveIntegerField('実行回数', default=0, editable=False)
    max_run_count = models.IntegerField('最大繰り返し回数', default=-1)

    def run(self, now):
        self.task.run()
        self.last_run_at = utils.get_now()
        self.total_run_count += 1
        self.next_time = utils.get_next_cron(self.cron_expr)
        self.save()

    def save(self, *args, **kwargs):
        update_next_time = not self.next_time
        if self.pk and hasattr(self, 'cron_expr'):
            old = self.__class__.objects.get(pk=self.pk)
            update_next_time = old.cron_expr != self.cron_expr
        if update_next_time:
            self.next_time = utils.get_next_cron(self.cron_expr)
        return super(CronSchedule, self).save(*args, **kwargs)

    def __str__(self):
        return '[{}] {} {} {}'.format(
            self.pk, self.name if self.name else '',
            self.cron_expr, self.task)


@python_2_unicode_compatible
class CeleryTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    task_id = models.CharField('タスクID', max_length=256, unique=True)

    task_path = models.CharField('タスク名', max_length=256, blank=True, null=True)
    args = models.TextField('引数', blank=True, null=True)
    kwargs = models.TextField('kw引数', blank=True, null=True)

    status = models.CharField(
        'ステータス', max_length=64, choices=TASK_STATE, default='sent')
    stack_trace = models.TextField('スタックトレース', blank=True, null=True)
    result_text = models.TextField('結果', blank=True, null=True)
    result_data = models.FileField(
        '結果ファイル', blank=True, null=True, storage=SimpleLazyObject(import_string(
            'heavy_celery.storage.CeleryTaskFileStorage')))

    created_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField(editable=False, blank=True, null=True)
    end_at = models.DateTimeField(editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    worker_id = models.CharField('ワーカーID', max_length=256, blank=True, null=True)

    def reexecute(self, **options):
        import_string(self.task_path).apply_async(
            args=yaml.load(self.args), kwargs=yaml.load(self.kwargs), **options)

    def revoke(self):
        if self.status == 'sent':
            self.status = 'cancel'
        else:
            self.status = 'revoking'
        celery_revoke(self.task_id, terminate=True)
        self.save()
