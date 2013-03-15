from settings_shared import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'lettuce.db',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': '',
    }
}

LETTUCE_SERVER_PORT = 8002
STATSD_HOST = '127.0.0.1'
BROWSER = 'Chrome'


# Running tests
#
# The checked in lettuce_base.db database is copied to lettuce.db
# at the beginning of each harvest
# You can modify the lettuce_base.db directly as needed to add base data
# You may also need to intermittenly need to do a migrate on lettuce_base.db
# as the database structure changes
#
# The base data includes
# * module_one/socialwork/ > Introduction, Quiz, Final
# * module_two/nutrition/ > Introduction, Counseling Sess 1, Counseling Sess 2
#
# Users
# * match_admin
# * match_participant_one
# * match_participant_two
#
# To run the tests
# ./manage.py harvest --settings=match.settings_test
