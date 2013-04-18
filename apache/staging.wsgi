import os, sys, site

site.addsitedir('/var/www/match/match/ve/lib/python2.7/site-packages')
sys.path.append('/var/www/match/match/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'match.settings_staging'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
