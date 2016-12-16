# Django settings for match project.
import os.path
from ccnmtlsettings.shared import common

project = 'match'
base = os.path.dirname(__file__)
locals().update(common(project=project, base=base))

PROJECT_APPS = ['match.main', 'match.nutrition']

TEMPLATES[0]['OPTIONS']['context_processors'].append(  # noqa
    'match.main.views.context_processor'
)

INSTALLED_APPS += [  # noqa
    'sorl.thumbnail',
    'pagetree',
    'pageblocks',
    'match.main',
    'quizblock',
    'careermapblock',
    'registration',
    'responseblock',
    'match.nutrition',
    'tastypie',
    'lettuce.django',
    'bootstrapform',
]

LETTUCE_APPS = (
    'match.main',
    'match.nutrition'
)

ACCOUNT_ACTIVATION_DAYS = 7

PAGEBLOCKS = [
    'pageblocks.HTMLBlockWYSIWYG',
    'pageblocks.TextBlock',
    'pageblocks.HTMLBlock',
    'pageblocks.PullQuoteBlock',
    'pageblocks.ImageBlock',
    'pageblocks.ImagePullQuoteBlock',
    'quizblock.Quiz',
    'careermapblock.CareerMap',
    'responseblock.Response',
    'nutrition.CounselingSession',
    'nutrition.CounselingReferral',
    'main.ImageMapChart',
]

THUMBNAIL_SUBDIR = "thumbs"
