# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import threading
from datetime import datetime

from django.conf import settings
from django.utils import timezone
# from django.utils.module_loading import import_string
from croniter import croniter


_app = None
_task = {}
_user = {}
_get_request = None


def set_task(task):
    _task[threading.current_thread()] = task
    _user[threading.current_thread()] = task.user


def reset_task():
    _task.pop(threading.current_thread(), None)
    _user.pop(threading.current_thread(), None)


def _return_none():
    return None


def get_user():
    global _get_request

    user = _user.get(threading.current_thread(), None)
    if user:
        return user

    if _get_request is None:
        if 'django_busybody.middlewares.GlobalRequestMiddleware' in settings.MIDDLEWARE_CLASSES:
            try:
                from django_busybody.tools import get_global_request
                _get_request = get_global_request
            except ImportError:
                _get_request = _return_none

        elif 'crequest.middleware.CrequestMiddleware' in settings.MIDDLEWARE_CLASSES:
            try:
                from crequest.middleware import CrequestMiddleware
                _get_request = CrequestMiddleware.get_request
            except ImportError:
                _get_request = _return_none

    request = _get_request()
    if request:
        return request.user
    return None


def get_now():
    return timezone.localtime(timezone.now()).replace(second=0, microsecond=0)


def get_next_cron(cron_expr, now=None):
    if now is None:
        now = get_now()
    return croniter(cron_expr, now).get_next(datetime)


class Logger(object):
    class F(object):
        def __init__(self, func, level_id):
            self.func = func
            self.level_id = level_id

        def __call__(self, *args, **kwargs):
            return self.func(self.level_id, *args, **kwargs)

    def __init__(self, task, root_logger, propagate):
        from .models import CeleryTaskLog
        self.root_logger = root_logger
        self.propagate = propagate
        self.task = task
        self.klass = CeleryTaskLog
        self._map = dict(self.klass.LEVEL_CHOICES)

        for level_id, level_string in self.klass.LEVEL_CHOICES:
            setattr(self, level_string, self.F(self._log, level_id))
            setattr(self, 'get_{}'.format(level_string), self.F(self._get_log, level_id))

    def _log(self, level, text):
        if self.propagate:
            getattr(self.root_logger, self._map[level])(text)
        self.klass.objects.create(task=self.task, level=level, text=text)

    def _get_log(self, level):
        return self.klass.objects.create(task=self.task, level=level, text="")


def get_logger(default_logger, propagate=True):
    t = _task.get(threading.current_thread(), None)
    if t:
        return Logger(t, default_logger, propagate)
    return default_logger
