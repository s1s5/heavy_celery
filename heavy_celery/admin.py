from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib import admin

from . import models


@admin.register(models.CronSchedule)
class CronScheduleAdmin(admin.ModelAdmin):
    model = models.CronSchedule
    list_display = ('id', 'name', 'cron_expr', 'task', 'next_time',
                    'expires', 'total_run_count', 'max_run_count')
    inline_reverse = ['task']


def execute_task_signature(modeladmin, request, queryset):
    for i in queryset:
        i.run()


execute_task_signature.short_description = "Taskを実行する"


@admin.register(models.TaskSignature)
class TaskSignatureAdmin(admin.ModelAdmin):
    model = models.TaskSignature
    list_display = ('id', 'name', 'task_path', 'args', 'kwargs', 'options')
    actions = [execute_task_signature, ]


def reexecute_tasks(modeladmin, request, queryset):
    for i in queryset:
        i.reexecute()


def cancel_revoke_tasks(modeladmin, request, queryset):
    for i in queryset:
        i.revoke()


reexecute_tasks.short_description = "Taskを再実行する"
cancel_revoke_tasks.short_description = "Taskをcancel/revokeする"


@admin.register(models.CeleryTask)
class CeleryTaskAdmin(admin.ModelAdmin):
    model = models.CeleryTask
    list_display = ('id', 'status', 'user', 'task_id', 'task_path',
                    'created_at', 'updated_at', 'start_at', 'end_at',
                    'result_text', 'result_data')
    list_filter = ('status', 'task_path', 'created_at')

    actions = [reexecute_tasks, cancel_revoke_tasks, ]
