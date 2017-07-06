# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from heavy_celery.urls import urlpatterns as heavy_celery_urls

urlpatterns = [
    url(r'^', include(heavy_celery_urls, namespace='heavy_celery')),
]
