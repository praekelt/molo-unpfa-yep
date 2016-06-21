from .base import * # noqa


DEBUG = True
TEMPLATE_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'AUTO_UPDATE': False,
    }
}

try:
    from .local import *
except ImportError:
    pass

try:
    from secrets import *
except ImportError:
    pass
