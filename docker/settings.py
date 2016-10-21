"""Django settings for use within the docker container."""

from os import environ

import dj_database_url

from .production import *  # noqa


def bool_env(val):
    """Replaces string based environment values with Python booleans"""
    return True if environ.get(val, False) == 'True' else False

# Disable debug mode

DEBUG = False

SECRET_KEY = environ.get('SECRET_KEY') or 'please-change-me'
PROJECT_ROOT = (
    environ.get('PROJECT_ROOT') or dirname(dirname(abspath(__file__))))

SERVICE_DIRECTORY_API_BASE_URL = environ.get(
    'SERVICE_DIRECTORY_API_BASE_URL', '')
SERVICE_DIRECTORY_API_USERNAME = environ.get(
    'SERVICE_DIRECTORY_API_USERNAME', '')
SERVICE_DIRECTORY_API_PASSWORD = environ.get(
    'SERVICE_DIRECTORY_API_PASSWORD', '')

GOOGLE_PLACES_API_SERVER_KEY = environ.get(
    'GOOGLE_PLACES_API_SERVER_KEY', '')

RAVEN_DSN = environ.get('RAVEN_DSN')
RAVEN_CONFIG = {'dsn': RAVEN_DSN} if RAVEN_DSN else {}

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///%s' % (join(PROJECT_ROOT, 'tunememolo.db'),))}

MEDIA_ROOT = join(PROJECT_ROOT, 'media')

STATIC_ROOT = join(PROJECT_ROOT, 'static')

LOCALE_PATHS = (
    join(PROJECT_ROOT, "locale"),
)

# until we can specify ES host in cluster
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.db.DBSearch',
    }
}

ENABLE_SERVICE_DIRECTORY = bool_env('ENABLE_SERVICE_DIRECTORY')
