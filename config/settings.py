"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config
from datetime import timedelta

# from ussd.store.journey_store import YamlJourneyStore

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rm7@5^)xz5by8z8zxs$vb2zpq+3g2=+y$z+uqtc(#1co_jz351'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False)

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.survey',
    'apps.message',
    'apps.common',
    'apps.subscriber',
    'apps.accounts',
    'apps.analytics',
    'apps.dhis',
    'rest_framework',
    'corsheaders',
    'knox',
    'django_celery_beat',
    'ussd',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.routing.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', None),
        'USER': config('DB_USER', None),
        'PASSWORD': config('DB_PASSWORD', None),
        'HOST': config('DB_HOST', None),
        'PORT': config('DB_PORT', None),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

DEFAULT_USSD_SCREEN_JOURNEY = "journeys/help.yaml"
# JOURNEY_STORE = YamlJourneyStore.YamlJourneyStore
# JOURNEY_STORE_CONFIG = dict(journey_directory=os.path.join(BASE_DIR, ".journeys"))

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000"
# ]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Addis_Ababa'
CELERY_BEAT_SCHEDULE = {
    'send-summary-every-hour': {
        'task': 'apps.survey.tasks.sync_survey_result_2_central_repo_task',
        # Executes every 30 minutes (30 minutes * 60 seconds)
        'schedule': timedelta(seconds=1800),
    },
    'generate-report': {
        'task': 'apps.analytics.tasks.generate_report',
        # Executes every 1 day (24 hrs * 60 minutes * 60 seconds)
        'schedule': timedelta(seconds=86400),
    },
    'copy-incomplete-data-2-survey-results': {
        'task': 'apps.survey.tasks.copy_incomplete_data_2_survey_results_task',
        # Execute every 30 minutes (30 minutes * 60 seconds)
        'schedule': timedelta(seconds=1800),
    },
    'clear-expired-session': {
        'task': 'apps.survey.tasks.clear_expired_session_task',
        # Execute every 10 minutes (10 minutes * 60 seconds)
        'schedule': timedelta(seconds=600),
    },
    'sync-dhis2-metadata': {
        'task': 'apps.dhis.tasks.sync_dhis2_metadata',
        # Executes every 7 day (7 days * 24 hrs * 60 minutes * 60 seconds)
        'schedule': timedelta(seconds=604800),
    },
    'cache-dhis2-metadata': {
        'task': 'apps.dhis.tasks.cache_dhis2_metadata',
        'schedule': timedelta(seconds=604800),
    },
    'sync-data-to-dhis2': {
        'task': 'apps.dhis.tasks.sync_data_to_dhis2',
        # Executes every 2 hours
        'schedule': timedelta(hours=2),
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [config('REDIS_URL', 'redis://redis:6379')]
        },
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'journeys')
MEDIA_URL = '/journeys/'

# To cache language of the subscriber on redis
REDIS_HOST = config('REDIS_HOST', 'redis')
REDIS_PORT = config('REDIS_PORT', 6379)

ADMINS = (
    ('admin', 'admin@example.com'),
)

CENTRAL_REPO_AUTH_URL = config('CENTRAL_REPO_AUTH_URL', None)
CENTRAL_REPO_CI_URL = config('CENTRAL_REPO_CI_URL', None)
CENTRAL_REPO_USERNAME = config('CENTRAL_REPO_USERNAME', None)
CENTRAL_REPO_PASSWORD = config('CENTRAL_REPO_PASSWORD', None)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
