# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.deconstruct import deconstructible


class Proxy(object):
    def __init__(self, backend):
        self.__dict__['_backend_string_'] = backend
        self.__dict__['_initialized_'] = False
        self.__dict__['_upper_'] = None

    def _prepare(self):
        if self.__dict__['_initialized_']:
            return
        self.__dict__['_initialized_'] = True
        self.__dict__['_upper_'] = import_string(self.__dict__['_backend_string_'])()

    def __getattr__(self, key):
        if '_constructor_args' == key:
            return self.__dict__[key]
        self._prepare()
        return getattr(self.__dict__['_upper_'], key)

    def __setattr__(self, key, value):
        if '_constructor_args' == key:
            self.__dict__[key] = value
            return
        self._prepare()
        return setattr(self.__dict__['_upper_'], key, value)


@deconstructible
class CeleryTaskFileStorage(Proxy):
    def __init__(self):
        super(CeleryTaskFileStorage, self).__init__(
            settings.CELERY_TASK_FILE_STORAGE if hasattr(settings, 'CELERY_TASK_FILE_STORAGE')
            else settings.DEFAULT_FILE_STORAGE)
