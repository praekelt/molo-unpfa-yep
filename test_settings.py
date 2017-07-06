from tuneme.settings import *  # noqa

SITE_LAYOUT = 'new'
TEMPLATES[0]['DIRS'] = [
    join(PROJECT_ROOT, 'tuneme', 'templates', SITE_LAYOUT), ]

INSTALLED_APPS += [
    'likes',
    'secretballot'
]

MIDDLEWARE_CLASSES += [
    'likes.middleware.SecretBallotUserIpUseragentMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'ndohyep_test.db',
    }
}
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.db',
    }
}
DEBUG = True
CELERY_ALWAYS_EAGER = True
