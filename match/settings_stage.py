# flake8: noqa
from settings_shared import *

ADMINS = (
    ('CCNMTL-Kang', 'ccnmtl-sysadmin+staging@columbia.edu'),
)

TEMPLATE_DIRS = (
    "/usr/local/share/sandboxes/common/match/match/match/templates",
)

MEDIA_ROOT = '/usr/local/share/sandboxes/common/match/uploads/'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

try:
    from local_settings import *
except ImportError:
    pass
