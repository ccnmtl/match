# flake8: noqa
from settings_shared import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'match',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

TEMPLATE_DIRS = (
    "/var/www/match/match/match/templates",
)

MEDIA_ROOT = '/var/www/match/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/match/match/sitemedia'),
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SENTRY_SITE = 'match-staging'
STATSD_PREFIX = 'match-staging'

SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

if 'migrate' not in sys.argv:
    import logging
    from sentry.client.handlers import SentryHandler
    logger = logging.getLogger()
    if SentryHandler not in map(lambda x: x.__class__, logger.handlers):
        logger.addHandler(SentryHandler())
        logger = logging.getLogger('sentry.errors')
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())

try:
    from local_settings import *
except ImportError:
    pass
