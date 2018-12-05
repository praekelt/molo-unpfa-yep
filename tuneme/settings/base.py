# -*- coding: utf-8 -*-
"""
Django settings for base tuneme.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from os.path import abspath, dirname, join
from os import environ
import django.conf.locale
from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _
import dj_database_url
import djcelery
from celery.schedules import crontab
djcelery.setup_loader()

# Absolute filesystem path to the Django project directory:
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v+*c@9@x%h%ou32gk58nv5=03dti0=z^g%296vcx*1alxg#m2)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENV = 'dev'

ALLOWED_HOSTS = ['*']


# Base URL to use when referring to full URLs within the Wagtail admin backend
# e.g. in notification emails. Don't include '/admin' or a trailing slash
# BASE_URL = 'http://example.com'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    'taggit',
    'modelcluster',

    'tuneme',
    'molo.core',
    'molo.profiles',
    'molo.surveys',
    'django_comments',
    'molo.commenting',
    'molo.yourwords',
    'molo.yourtips',
    'molo.servicedirectory',
    'molo.globalsite',

    'molo.pwa',
    'fcm_django',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailsites',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
    'wagtailmedia',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    'wagtailsurveys',
    'wagtail.contrib.wagtailsitemaps',
    'wagtail_personalisation',

    'mptt',
    'django.contrib.sites',
    'google_analytics',

    'raven.contrib.django.raven_compat',
    'djcelery',
    'django_cas_ng',
    'compressor',
    'notifications',
    'el_pagination',

    'secretballot',
    'likes',
    'storages',
    'import_export'
]

COMMENTS_APP = 'molo.commenting'
COMMENTS_FLAG_THRESHHOLD = 3
COMMENTS_HIDE_REMOVED = False

SITE_ID = 1

# We have multiple layouts: use `old` or `new` to switch between them.
SITE_LAYOUT = environ.get('SITE_LAYOUT', 'new')

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'molo.core.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',

    'molo.core.middleware.AdminLocaleMiddleware',
    'molo.core.middleware.NoScriptGASessionMiddleware',
    'molo.core.middleware.MoloGoogleAnalyticsMiddleware',
    'molo.core.middleware.MultiSiteRedirectToHomepage',

    'molo.globalsite.middleware.CountrySiteRedirectMiddleware',

    'likes.middleware.SecretBallotUserIpUseragentMiddleware'
]

AUTHENTICATION_BACKENDS = [
    'molo.profiles.backends.MoloProfilesModelBackend',
    'molo.core.backends.MoloModelBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(PROJECT_ROOT, 'tuneme', 'templates', SITE_LAYOUT), ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'molo.core.context_processors.locale',
                'molo.profiles.context_processors.get_profile_data',
                'molo.core.processors.compress_settings',
                'wagtail.contrib.settings.context_processors.settings',
                'tuneme.context_processors.default_forms',
                'tuneme.context_processors.add_tag_manager_account',
                'tuneme.context_processors.detect_freebasics',
                'tuneme.processors.compress_settings',

                'molo.servicedirectory.context_processors'
                '.enable_service_directory_context',
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "mote.loaders.app_directories.Loader",
                "django.template.loaders.app_directories.Loader",
            ]
        },

    },
]

ROOT_URLCONF = 'tuneme.urls'
WSGI_APPLICATION = 'tuneme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# SQLite (simplest install)
DATABASES = {'default': dj_database_url.config(
    default='sqlite:///%s' % (join(PROJECT_ROOT, 'db.sqlite3'),))}

# PostgreSQL (Recommended, but requires the psycopg2 library and
#             Postgresql development headers)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'base',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': '',  # Set to empty string for localhost.
#         'PORT': '',  # Set to empty string for default.
#         # number of seconds database connections should persist for
#         'CONN_MAX_AGE': 600,
#     }
# }

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ('molo.profiles.task', 'molo.core.tasks',
                  'google_analytics.tasks')
BROKER_URL = environ.get('BROKER_URL', '')
CELERY_RESULT_BACKEND = environ.get(
    'CELERY_RESULT_BACKEND', '')
CELERYBEAT_SCHEDULE = {
    'rotate_content': {
        'task': 'molo.core.tasks.rotate_content',
        'schedule': crontab(minute=0),
    },
    'molo_consolidated_minute_task': {
        'task': 'molo.core.tasks.molo_consolidated_minute_task',
        'schedule': crontab(minute='*'),
    },
}
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = environ.get('LANGUAGE_CODE', 'en')
TIME_ZONE = 'Africa/Johannesburg'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Native South African languages are currently not included in the default
# list of languges in django
# https://github.com/django/django/blob/master/django/conf/global_settings.py#L50
LANGUAGES = global_settings.LANGUAGES + [
    ('zu', _('Zulu')),
    ('xh', _('Xhosa')),
    ('st', _('Sotho')),
    ('ve', _('Venda')),
    ('tn', _('Tswana')),
    ('ts', _('Tsonga')),
    ('ss', _('Swati')),
    ('nr', _('Ndebele')),
    ('bem', _('Bemba')),
    ('nya', _('Nyanja')),
    ('ny', _('Chichewa')),
]

EXTRA_LANG_INFO = {
    'zu': {
        'bidi': False,
        'code': 'zu',
        'name': 'Zulu',
        'name_local': 'isiZulu',
    },
    'xh': {
        'bidi': False,
        'code': 'xh',
        'name': 'Xhosa',
        'name_local': 'isiXhosa',
    },
    'st': {
        'bidi': False,
        'code': 'st',
        'name': 'Sotho',
        'name_local': 'seSotho',
    },
    've': {
        'bidi': False,
        'code': 've',
        'name': 'Venda',
        'name_local': u'tshiVenḓa',
    },
    'tn': {
        'bidi': False,
        'code': 'tn',
        'name': 'Tswana',
        'name_local': 'Setswana',
    },
    'ts': {
        'bidi': False,
        'code': 'ts',
        'name': 'Tsonga',
        'name_local': 'xiTsonga',
    },
    'ss': {
        'bidi': False,
        'code': 'ss',
        'name': 'Swati',
        'name_local': 'SiSwati',
    },
    'nr': {
        'bidi': False,
        'code': 'nr',
        'name': 'Ndebele',
        'name_local': 'isiNdebele',
    },
    'bem': {
        'bidi': False,
        'code': 'bem',
        'name': 'Bemba',
        'name_local': 'Bemba',
    },
    'nya': {
        'bidi': False,
        'code': 'nya',
        'name': 'Nyanja',
        'name_local': 'Nyanja',
    },
    'ny': {
        'bidi': False,
        'code': 'ny',
        'name': 'Chichewa',
        'name_local': 'Chichewa',
    }
}


django.conf.locale.LANG_INFO.update(EXTRA_LANG_INFO)

LOCALE_PATHS = [
    join(PROJECT_ROOT, "locale"),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
COMPRESS_ENABLED = True

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'


MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

FROM_EMAIL = environ.get('FROM_EMAIL', "support@moloproject.org")
CONTENT_IMPORT_SUBJECT = environ.get(
    'CONTENT_IMPORT_SUBJECT', 'Molo Content Import')
CONTENT_COPY_SUBJECT = environ.get(
    'CONTENT_COPY_SUBJECT', 'Molo Content Copy')
CONTENT_COPY_FAILED_SUBJECT = environ.get(
    'CONTENT_COPY_FAILED_SUBJECT', 'Molo Content Copy Failed')

# Wagtail settings

LOGIN_URL = 'molo.profiles:auth_login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'

SITE_NAME = environ.get('SITE_NAME', "TuneMe")
WAGTAIL_SITE_NAME = SITE_NAME

# Whether to use face/feature detection to improve image
# cropping - requires OpenCV
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False

# Use Elasticsearch as the search backend for extra performance and
# better search results:
# http://wagtail.readthedocs.org/en/latest/howto/performance.html#search
# http://wagtail.readthedocs.org/en/latest/core_components/search/backends.html#elasticsearch-backend  # noqa
#
WAGTAILSEARCH_RESULTS_TEMPLATE = 'search/search_results.html'

# NOTE: We're falling back to the DB backend because multi-language filtering
# requires us to filter on a related field which is not currently supported
# by Wagtail (http://docs.wagtail.io/en/v1.5.2/topics/search/indexing.html)
# Filtering on index.RelatedFields with the QuerySet API is planned for a future release of Wagtail. # noqa

# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': (
#             'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch'),
#         'INDEX': 'tuneme',
#         'AUTO_UPDATE': True,
#     },
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'import_console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'import_logger': {
            'handlers': ['import_console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

ES_HOST = environ.get('ES_HOST')
ES_INDEX = environ.get('ES_INDEX')
ES_VERSION = int(environ.get('ES_VERSION', 5))

ES_BACKEND_V1 = 'wagtail.wagtailsearch.backends.elasticsearch'
ES_BACKEND_V2 = 'wagtail.wagtailsearch.backends.elasticsearch2'
ES_BACKEND_V5 = 'wagtail.wagtailsearch.backends.elasticsearch5'

if ES_VERSION == 5:
    SELECTED_ES_BACKEND = ES_BACKEND_V5
elif ES_VERSION == 2:
    SELECTED_ES_BACKEND = ES_BACKEND_V2
else:
    SELECTED_ES_BACKEND = ES_BACKEND_V1

ES_SELECTED_INDEX = ES_INDEX or environ.get('MARATHON_APP_ID', '')

if ES_HOST and ES_SELECTED_INDEX:
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': SELECTED_ES_BACKEND,
            'URLS': [ES_HOST],
            'INDEX': ES_SELECTED_INDEX.replace('/', '')
        },
    }

# Whether to use face/feature detection to improve image cropping - requires OpenCV  # noqa
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False

ADMIN_LANGUAGE_CODE = environ.get('ADMIN_LANGUAGE_CODE', "en")

GOOGLE_TAG_MANAGER_ACCOUNT = environ.get('GOOGLE_TAG_MANAGER_ACCOUNT')
CUSTOM_UIP_HEADER = 'HTTP_X_IORG_FBS_UIP'

GOOGLE_ANALYTICS = {}
GOOGLE_ANALYTICS_IGNORE_PATH = [
    # health check used by marathon
    '/health/',
    # admin interfaces for wagtail and django
    '/admin/', '/django-admin/',
    # Universal Core content import URL
    '/import/',
    # browser troll paths
    '/favicon.ico', '/robots.txt',
    # when using nginx, we handle statics and media
    # but including them here just incase
    '/media/', '/static/',
    # metrics URL used by promethius monitoring system
    '/metrics',
    # REST API endpoints
    '/api/',
    # PWA serviceworker
    '/serviceworker.js',
]

CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH = environ.get(
    'GOOGLE_ANALYTICS_IGNORE_PATH')
if CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH:
    GOOGLE_ANALYTICS_IGNORE_PATH += [
        d.strip() for d in CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH.split(',')]

CSRF_FAILURE_VIEW = 'molo.core.views.csrf_failure'

FREE_BASICS_URL_FOR_CSRF_MESSAGE = environ.get(
    'FREE_BASICS_URL_FOR_CSRF_MESSAGE', '')

ENABLE_SSO = False

AWS_HEADERS = {
    # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}
# Amazon S3 bucket settings
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

if AWS_STORAGE_BUCKET_NAME and AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Google cloud bucket settings
GS_BUCKET_NAME = environ.get('GS_BUCKET_NAME', '')
GS_CREDENTIALS_FILE = environ.get('GS_CREDENTIALS_FILE', '')

if GS_BUCKET_NAME and GS_CREDENTIALS_FILE:
    from google.oauth2 import service_account
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        GS_CREDENTIALS_FILE)
    MEDIA_URL = "https://storage.cloud.google.com/%s/" % GS_BUCKET_NAME
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

PWA_SERVICE_WORKER_PATH = join(
    PROJECT_ROOT, 'tuneme', 'templates', SITE_LAYOUT, 'serviceworker.js')
PWA_NAME = 'Tuneme'
PWA_DESCRIPTION = "Tuneme"
PWA_THEME_COLOR = '#000000'
PWA_DISPLAY = 'standalone'
PWA_START_URL = '/'
PWA_ICONS = [
    {
        "src": "static/new/favicon/android-icon-96x96.png",
        "sizes": "96x96",
        "type": "image/png"
    },
    {
        "src": "static/new/favicon/android-icon-144x144.png",
        "sizes": "144x144",
        "type": "image/png"
    },
    {
        "src": "static/new/favicon/android-icon-192x192.png",
        "sizes": "192x192",
        "type": "image/png"
    }
]
PWA_FCM_API_KEY = 'AIzaSyDZ2wk0aUry81OKqW7BqjXWOzLEUax279Q'
PWA_FCM_MSGSENDER_ID = '756558445116'
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAsCZlujw:APA91bF4KmOWhc-rxeIM4C4Hq5kiLJDGH-D4EzRJPbR"
                      "etJ8AZV0nICx8csbaTwR7zfIzNVbbjHlv6Fnp_bAxo23SEjGzv99YSW"
                      "tFZucgQCKKoqgci8da-9eijVt56ikKZXhir0Xfonkv",
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": False,
}

# https://github.com/wagtail/wagtail/issues/3883
AWS_S3_FILE_OVERWRITE = False

# Global Site
GLOBAL_SITE_URL = environ.get('GLOBAL_SITE_URL', '')
GEOIP_PATH = join(dirname(dirname(abspath(__file__))), 'geoip_db')
GLOBAL_SITE_IGNORE_PATH = environ.get('GLOBAL_SITE_IGNORE_PATH', '')

SERVICE_DIRECTORY_RADIUS_OPTIONS = (
    (10, '10 km or less'),
    (25, '25 km or less'),
    (50, '50 km or less'),
    (100, '100 km or less')
)
