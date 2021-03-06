# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 11:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import heavy_celery.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=256, unique=True, verbose_name='タスクID')),
                ('task_path', models.CharField(blank=True, max_length=256, null=True, verbose_name='タスク名')),
                ('args', models.TextField(blank=True, null=True, verbose_name='引数')),
                ('kwargs', models.TextField(blank=True, null=True, verbose_name='kw引数')),
                ('status', models.CharField(choices=[('sent', 'PENDING'), ('received', 'RECEIVED'), ('started', 'STARTED'), ('failed', 'FAILURE'), ('retried', 'RETRY'), ('succeeded', 'SUCCESS'), ('revoked', 'REVOKED'), ('rejected', 'REJECTED'), ('cancel', 'CANCEL'), ('cancelled', 'CANCELLED'), ('revoking', 'REVOKING'), ('retry_rejected', 'RETRY_REJECTED')], default='sent', max_length=64, verbose_name='ステータス')),
                ('stack_trace', models.TextField(blank=True, null=True, verbose_name='スタックトレース')),
                ('result_string', models.TextField(blank=True, null=True, verbose_name='結果')),
                ('result_file', models.FileField(blank=True, null=True, storage=heavy_celery.storage.CeleryTaskFileStorage(), upload_to='', verbose_name='結果ファイル')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('end_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CeleryTaskLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('level', models.IntegerField(choices=[(0, 'debug'), (1, 'info'), (2, 'warning'), (3, 'error'), (4, 'critical'), (5, 'exception')])),
                ('text', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heavy_celery.CeleryTask')),
            ],
        ),
        migrations.CreateModel(
            name='CronSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='名前')),
                ('description', models.TextField(blank=True, null=True, verbose_name='詳細')),
                ('cron_expr', models.CharField(max_length=256, verbose_name='cron')),
                ('next_time', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expires', models.DateTimeField(blank=True, null=True, verbose_name='有効期限')),
                ('last_run_at', models.DateTimeField(blank=True, null=True, verbose_name='最終実行日時')),
                ('total_run_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='実行回数')),
                ('max_run_count', models.IntegerField(default=-1, verbose_name='最大繰り返し回数')),
            ],
        ),
        migrations.CreateModel(
            name='TaskSignature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='名前')),
                ('description', models.TextField(blank=True, null=True, verbose_name='詳細')),
                ('task_path', models.CharField(max_length=256, verbose_name='タスク名')),
                ('args', models.TextField(blank=True, null=True, verbose_name='引数')),
                ('kwargs', models.TextField(blank=True, null=True, verbose_name='kw引数')),
                ('options', models.TextField(blank=True, null=True, verbose_name='タスクオプション')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_id', models.CharField(max_length=256, verbose_name='ワーカーID')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('beated_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, '開始'), (1, '停止'), (2, '応答なし')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WorkerTaskLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=256, unique=True)),
                ('task_path', models.CharField(max_length=256)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heavy_celery.Worker')),
            ],
        ),
        migrations.AddField(
            model_name='cronschedule',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heavy_celery.TaskSignature'),
        ),
    ]
