from tuneme.settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'ndohyep_test.db',
    }
}
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.db.DBSearch',
    }
}
DEBUG = True
CELERY_ALWAYS_EAGER = True

SITE_LAYOUT = 'old'
