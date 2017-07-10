# -*- coding: utf-8 -*-

"""
Django settings for example project.

Generated by Cookiecutter Django Package

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(__file__)
PROJECT_NAME = os.path.basename(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "@r$-gj!^$8e(0=ww7pd&tgayxm+@(b+(z3##!cm64m6shj_s=4"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'heavy_celery',

    # if your app has other dependencies that need to be added to the site
    # they should be added here
]
SESSION_COOKIE_NAME = '{}-sessionid'.format(PROJECT_NAME)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

############################################
# log
############################################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
            'datefmt': '%y %b %d, %H:%M:%S',
        },
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(module)s '
                       '%(process)d %(thread)d %(message)s'),
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'heavy_celery': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        os.path.basename(PROJECT_NAME): {
            'handlers': ['console', ],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['console', ],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

db_type = os.environ.get('DB_TYPE', 'sqlite')
if db_type == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
elif db_type == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
            'HOST': os.environ.get('DB_ADDR', 'db'),
            'PORT': os.environ.get('DB_PORT', 5432),
        }
    }
else:
    raise Exception('unknown database type "{}"'.format(db_type))

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


############################################
# Internationalization
############################################
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
if sys.version_info[0] == 2:
    class JST(datetime.tzinfo):
        def utcoffset(self, dt):
            return datetime.timedelta(hours=9)

        def tzname(self, dt):
            return "Asia/Tokyo"

        def dst(self, dt):
            return datetime.timedelta(0)
    TZ_INFO = JST()
else:
    TZ_INFO = datetime.timezone(datetime.timedelta(hours=9))
USE_I18N = True
USE_L10N = True
USE_TZ = True


############################################
# cache
############################################
cache_type = os.environ.get('CACHE_TYPE', 'filebased')

# テストの時は基本的にはcacheをOFFにしておく
# if MODE == 'test':
#     cache_type = 'dummy'

if cache_type == 'memcached':
    CACHE_DEFAULT = dict(
        BACKEND='django.core.cache.backends.memcached.MemcachedCache',
        LOCATION='{}:{}'.format(
            os.environ.get('MEMCACHED_HOST', '127.0.0.1'),
            os.environ.get('MEMCACHED_PORT', '11211'),
        ),
    )
elif cache_type == 'redis':
    CACHE_DEFAULT = {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [
            '{}:{}'.format(os.environ.get('REDIS_CACHE_HOST', 'redis'),
                           os.environ.get('REDIS_CACHE_PORT', 6379), ),
        ],
        'OPTIONS': {
            'DB': os.environ.get('REDIS_CACHE_DB', 1),
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': -1,
        },
    }
elif cache_type == 'filebased':
    CACHE_DEFAULT = dict(
        BACKEND='django.core.cache.backends.filebased.FileBasedCache',
        LOCATION=os.environ.get('CACHE_FILEBASED_LOCATION', '/tmp/django_{}_cache/'.format(PROJECT_NAME)),
        OPTIONS={
            'MAX_ENTRIES': 32768,
        }
    )
elif cache_type == 'localmem':
    CACHE_DEFAULT = dict(
        BACKEND='django.core.cache.backends.locmem.LocMemCache',
        LOCATION='unique-{}-key'.format(PROJECT_NAME),
    )
elif cache_type == 'dummy':
    CACHE_DEFAULT = dict(
        BACKEND='django.core.cache.backends.dummy.DummyCache',
    )
else:
    raise Exception("unknown cache type : {}".format(cache_type))
CACHES = {
    'default': CACHE_DEFAULT,
}

############################################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

############################################
# Redis
############################################
REDIS_CELERY_PORT = os.environ.get('REDIS_CELERY_PORT', 6379)
REDIS_CELERY_DB = os.environ.get('REDIS_CELERY_DB', 2)
REDIS_CELERY_HOST = os.environ.get('REDIS_CELERY_HOST', 'redis')

############################################
# rabbit mq
############################################
RABBIT_HOSTNAME = os.environ.get('RABBIT_HOSTNAME', '127.0.0.1:5672')

if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

BROKER_URL = os.environ.get('BROKER_URL', '')
if not BROKER_URL:
    BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}'.format(
        user=os.environ.get('RABBIT_USER', PROJECT_NAME),
        password=os.environ.get('RABBIT_PASS', PROJECT_NAME),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_VHOST', PROJECT_NAME))

# We don't want to have dead connections stored on rabbitmq, so we have to
# negotiate using heartbeats
# BROKER_HEARTBEAT = '?heartbeat=180'
# if not BROKER_URL.endswith(BROKER_HEARTBEAT):
#     BROKER_URL += BROKER_HEARTBEAT
# BROKER_POOL_LIMIT = 1
# BROKER_CONNECTION_TIMEOUT = 10

############################################
# Celery configuration
############################################
from kombu import Exchange, Queue  # NOQA
# Sensible settings for celery
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

# By default we will ignore result
# If you want to see results and try out tasks interactively, change it to False
# Or change this setting on tasks level
# CELERY_RESULT_PERSISTENT = True
# CELERY_IGNORE_RESULT = False
CELERY_TASK_RESULT_EXPIRES = 600

# Set redis as celery result backend
CELERY_RESULT_BACKEND = 'redis://{}:{}/{}'.format(
    REDIS_CELERY_HOST, REDIS_CELERY_PORT, REDIS_CELERY_DB)
CELERY_REDIS_MAX_CONNECTIONS = 128

# Don't use pickle as serializer, json is much safer
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['application/json']

CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 1000

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('time_sensitive', Exchange('time_sensitive'), routing_key='time_sensitive_tasks'),
)

############################################
# current project
############################################
INSTALLED_APPS += [
    'django_celery_beat',

    'example.apps.sample',
]
