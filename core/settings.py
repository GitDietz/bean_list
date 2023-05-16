"""
Django settings for core project.
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import logging

from .base import *  # noqa
from .base import env

log = logging.getLogger('lista')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    "django.contrib.sites",
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_celery_beat",
    "django_bootstrap5",
    "django_filters",
    "bootstrap_datepicker_plus",
    'bootstrap_modal_forms',
    'widget_tweaks',
    'django_tables2',
    'storages',
]

LOCAL_APPS = [
    # ".users",
    'images.apps.ImagesConfig',
    'la.apps.LaConfig',
    'bill.apps.BillConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# S3 setup
if 'AWS_STORAGE_BUCKET_NAME' in os.environ:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_REGION_NAME = os.environ['AWS_S3_REGION_NAME']

    AWS_S3_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_S3_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL"), }

DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tables https://django-tables2.readthedocs.io/en/latest/index.html

DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap4.html'

# Static files (CSS, JavaScript, Images) ------------------
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'core/static',
]

# SECURITY ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"
# CSRF_FAILURE_VIEW = 'core.views.csrf_failure'

# CACHES ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}