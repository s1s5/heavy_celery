# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 00:52
from __future__ import unicode_literals

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


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
                ('task_id', models.CharField(max_length=256, unique=True, verbose_name='\u30bf\u30b9\u30afID')),
                ('task_path', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u30bf\u30b9\u30af\u540d')),
                ('args', models.TextField(blank=True, null=True, verbose_name='\u5f15\u6570')),
                ('kwargs', models.TextField(blank=True, null=True, verbose_name='kw\u5f15\u6570')),
                ('status', models.CharField(choices=[('sent', 'PENDING'), ('received', 'RECEIVED'), ('started', 'STARTED'), ('failed', 'FAILURE'), ('retried', 'RETRY'), ('succeeded', 'SUCCESS'), ('revoked', 'REVOKED'), ('rejected', 'REJECTED'), ('cancel', 'CANCEL'), ('cancelled', 'CANCELLED'), ('revoking', 'REVOKING'), ('retry_rejected', 'RETRY_REJECTED')], default='sent', max_length=64, verbose_name='\u30b9\u30c6\u30fc\u30bf\u30b9')),
                ('stack_trace', models.TextField(blank=True, null=True, verbose_name='\u30b9\u30bf\u30c3\u30af\u30c8\u30ec\u30fc\u30b9')),
                ('result_string', models.TextField(blank=True, null=True, verbose_name='\u7d50\u679c')),
                ('result_file', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(), upload_to=b'', verbose_name='\u7d50\u679c\u30d5\u30a1\u30a4\u30eb')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('end_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CronSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u540d\u524d')),
                ('description', models.TextField(blank=True, null=True, verbose_name='\u8a73\u7d30')),
                ('cron_expr', models.CharField(max_length=256, verbose_name='cron')),
                ('next_time', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expires', models.DateTimeField(blank=True, null=True, verbose_name='\u6709\u52b9\u671f\u9650')),
                ('last_run_at', models.DateTimeField(blank=True, null=True, verbose_name='\u6700\u7d42\u5b9f\u884c\u65e5\u6642')),
                ('total_run_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='\u5b9f\u884c\u56de\u6570')),
                ('max_run_count', models.IntegerField(default=-1, verbose_name='\u6700\u5927\u7e70\u308a\u8fd4\u3057\u56de\u6570')),
            ],
        ),
        migrations.CreateModel(
            name='TaskSignature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u540d\u524d')),
                ('description', models.TextField(blank=True, null=True, verbose_name='\u8a73\u7d30')),
                ('task_path', models.CharField(max_length=256, verbose_name='\u30bf\u30b9\u30af\u540d')),
                ('args', models.TextField(blank=True, null=True, verbose_name='\u5f15\u6570')),
                ('kwargs', models.TextField(blank=True, null=True, verbose_name='kw\u5f15\u6570')),
                ('options', models.TextField(blank=True, null=True, verbose_name='\u30bf\u30b9\u30af\u30aa\u30d7\u30b7\u30e7\u30f3')),
            ],
        ),
        migrations.AddField(
            model_name='cronschedule',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heavy_celery.TaskSignature'),
        ),
    ]
