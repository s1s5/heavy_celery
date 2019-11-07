=============================
heavy_celery
=============================

.. image:: https://badge.fury.io/py/heavy_celery.svg
    :target: https://badge.fury.io/py/heavy_celery

.. image:: https://travis-ci.org/s1s5/heavy_celery.svg?branch=master
    :target: https://travis-ci.org/s1s5/heavy_celery

.. image:: https://codecov.io/gh/s1s5/heavy_celery/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/s1s5/heavy_celery

managed celery task

Documentation
-------------

The full documentation is at https://heavy_celery.readthedocs.io.

Quickstart
----------

Install heavy_celery::

    pip install heavy_celery

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'heavy_celery',
        ...
    )

Features
--------

settings.py
-----------

.. code-block:: python

    CELERY_DEFAULT_QUEUE = 'default'
    CELERY_DEFAULT_EXCHANGE_TYPE = 'default'
    CELERY_DEFAULT_ROUTING_KEY = 'default'
    
    CELERY_QUEUES = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('time_sensitive', Exchange('time_sensitive'), routing_key='time_sensitive_tasks'),
        Queue('background', Exchange('background'), routing_key='background'),
    )

    CELERY_REVOKE = 'example.apps.sample.tasks.celery_revoke'  # 適当なモジュールパスに変更
    MIDDLEWARE += [
        'heavy_celery.middlewares.GlobalRequestMiddleware',
    ]


example/apps/sample/tasks.py
----------------------------

.. code-block:: python

    @app.task()
    def celery_revoke(task_id):
        from celery.task.control import revoke
        revoke(task_id, terminate=True)


cronの機能を使うために
----------------------

.. code-block:: python
    
    from celery.schedules import crontab
    from <project_name>.celery_conf import app
    from heavy_celery.cron import spawner as _cron_scheduler
    
    @app.task()
    def cron_scheduler():
        _cron_scheduler()
    
    app.conf.beat_schedule = {
        'cron_scheduler': {
            'task': '<appname>.tasks.cron_scheduler',
            'schedule': crontab(),
            'args': (),
            'options': dict(queue='time_sensitive', routing_key='time_sensitive_tasks'),
        },
    }


task定義の仕方
--------------

.. code-block:: python

    from heavy_celery import base
    
    @app.task(base=base.Task)
    def command(command_name, *args, **kw):
        call_command(command_name, *args, **kw)


タスクの定期実行のやり方
------------------------

- TaskSignatureの追加

 - name : タスク名
 - description : タスク詳細
 - task_path : タスクパス e.g) apps.foo.tasks.example_task
 - args : タスクに渡す引数(yaml形式)
 - kwargs : タスクに渡すkw引数(yaml形式)
 - options : タスクのスケジュールオプション、どのQueueにいれるかとか
   したみたいにしておけば、time_sensitiveのQueueで走るようになる

  - queue: time_sensitive
    routing_key: time_sensitive_tasks

- CronScheduleの追加

 - name : cronタスク名
 - description : cronタスク詳細
 - cron_expr : cron表記
 - task : TaskSignatureオブジェクト
 - max_run_count : 最大繰り返し回数


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage


Development
-----------

    $ cookiecutter https://github.com/pydanny/cookiecutter-djangopackage

    $ mkvirtualenv --no-site-packages heavy_celery
    $ pip install tox twine

    # test
    $ make test-all

    # release
    $ python setup.py publish  # at first
    $ pip install readme_renderer  # at first
    $ python setup.py check -r -s   # syntax check
    $ make release
