# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import uuid
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
_worker_id = None


def set_task(task):
    task.worker_id = get_worker_id()
    task.save(update_fields=['worker_id'])
    _task[threading.current_thread()] = task
    _user[threading.current_thread()] = task.user


def reset_task():
    _task.pop(threading.current_thread(), None)
    _user.pop(threading.current_thread(), None)


def get_worker_id():
    global _worker_id
    if _worker_id is None:
        _worker_id = uuid.uuid4().hex
    return _worker_id


def _return_none():
    return None


def get_user():
    global _get_request

    user = _user.get(threading.current_thread(), None)
    if user:
        return user

    MIDDLEWARE = settings.MIDDLEWARE
    if MIDDLEWARE is None:
        MIDDLEWARE = settings.MIDDLEWARE_CLASSES

    if _get_request is None:
        _get_request = _return_none
        if 'django_busybody.middlewares.GlobalRequestMiddleware' in MIDDLEWARE:
            try:
                from django_busybody.tools import get_global_request
                _get_request = get_global_request
            except ImportError:
                pass

        elif 'crequest.middleware.CrequestMiddleware' in MIDDLEWARE:
            try:
                from crequest.middleware import CrequestMiddleware
                _get_request = CrequestMiddleware.get_request
            except ImportError:
                pass

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
