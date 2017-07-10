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
        'heavy_celery.apps.HeavyCeleryConfig',
        ...
    )

Add heavy_celery's URL patterns:

.. code-block:: python

    from heavy_celery import urls as heavy_celery_urls


    urlpatterns = [
        ...
        url(r'^', include(heavy_celery_urls)),
        ...
    ]

Features
--------

* TODO

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
    $ make release
