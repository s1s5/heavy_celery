=====
Usage
=====

To use heavy_celery in a project, add it to your `INSTALLED_APPS`:

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
