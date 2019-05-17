# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import time
import json


from ... import tasks
from heavy_celery import models as hc_models

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        hc_models.CronSchedule.objects.all().delete()
        hc_models.TaskSignature.objects.all().delete()
        time.sleep(5)
        hc_models.CeleryTask.objects.all().delete()

        task_args = ('task', 1, 3.0)
        task_kwargs = {'hello': 'world', 'foo': 3, 'var': 9.0}
        tasks.hello_world.delay(*task_args, **task_kwargs)
        tasks.test_exception.delay(*task_args, **task_kwargs)
        tasks.hello_world2.delay(*task_args, **task_kwargs)
        tasks.create_file.delay(*task_args, **task_kwargs)
        tasks.create_file2.delay(*task_args, **task_kwargs)

        for try_cnt in range(100):
            time.sleep(1)
            if hc_models.CeleryTask.objects.all().count() == 5:
                break
        time.sleep(30)

        # create_file_result = 'args={} kwargs={}'.format(task_args, task_kwargs)

        ct = hc_models.CeleryTask.objects.get(task_path='example.apps.sample.tasks.hello_world')
        print(ct.status, ct.result_text)
        # assert ct.status == 'succeeded'
        # assert ct.result_text == json.dumps('hello world')

        ct = hc_models.CeleryTask.objects.get(task_path='example.apps.sample.tasks.test_exception')
        assert ct.status == 'failed'

        ct = hc_models.CeleryTask.objects.get(task_path='example.apps.sample.tasks.hello_world2')
        print(ct.status, ct.result_text)
        # assert ct.status == 'succeeded'
        # assert ct.result_text == json.dumps('hello world2')

        ct = hc_models.CeleryTask.objects.get(task_path='example.apps.sample.tasks.create_file')
        print(ct.status, ct.result_data.read())
        # assert ct.status == 'succeeded'
        # assert ct.result_data.read() == create_file_result, 'example.apps.sample.tasks.create_file failed'

        ct = hc_models.CeleryTask.objects.get(task_path='example.apps.sample.tasks.create_file2')
        print(ct.status, ct.result_data.read())
        # assert ct.status == 'succeeded'
        # assert ct.result_data.read() == create_file_result, 'example.apps.sample.tasks.create_file2 failed'
