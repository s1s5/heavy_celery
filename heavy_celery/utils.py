# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import threading
from datetime import datetime

# from django.conf import settings
from django.utils import timezone
# from django.utils.module_loading import import_string
from croniter import croniter


_app = None
_user = {}
_middleware = None


def set_user(user):
    _user[threading.current_thread()] = user


def reset_user():
    _user.pop(threading.current_thread(), None)


def get_user():
    global _middleware

    user = _user.get(threading.current_thread(), None)
    if user:
        return user

    if _middleware is None:
        try:
            from crequest.middleware import CrequestMiddleware
        except ImportError:
            class CrequestMiddleware(object):
                @classmethod
                def get_request(klass):
                    return None
        _middleware = CrequestMiddleware

    request = _middleware.get_request()
    if request:
        return request.user
    return None


def get_now():
    return timezone.localtime(timezone.now()).replace(second=0, microsecond=0)


def get_next_cron(cron_expr, now=None):
    if now is None:
        now = get_now()
    return croniter(cron_expr, now).get_next(datetime)
