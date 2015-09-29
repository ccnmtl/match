from django.conf.urls import patterns, include
from django.contrib import admin
from django.conf import settings
import os.path
from django.views.generic import TemplateView
admin.autodiscover()


site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)

auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))

logout_page = (r'^accounts/logout/$',
               'django.contrib.auth.views.logout',
               {'next_page': redirect_after_logout})
admin_logout_page = (r'^accounts/logout/$',
                     'django.contrib.auth.views.logout',
                     {'next_page': '/admin/'})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (r'^accounts/logout/$',
                   'djangowind.views.logout',
                   {'next_page': redirect_after_logout})
    admin_logout_page = (r'^admin/logout/$',
                         'djangowind.views.logout',
                         {'next_page': redirect_after_logout})

urlpatterns = patterns(
    '',
    logout_page,
    admin_logout_page,
    auth_urls,
    (r'^$', 'match.main.views.intro'),
    (r'^intro/$', 'match.main.views.intro'),
    (r'^about/$', 'match.main.views.background', {'content_to_show': 'about'}),
    (r'^help/$', 'match.main.views.background', {'content_to_show': 'help'}),
    ('^admin/allresults/$', 'match.main.views.all_results'),
    ('^admin/allresultskey/$', 'match.main.views.all_results_key'),
    (r'^admin/', include(admin.site.urls)),
    (r'^registration/', include('registration.urls')),
    (r'^smoketest/', include('smoketest.urls')),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^_quiz/', include('quizblock.urls')),
    (r'^_careermap/', include('careermapblock.urls')),
    (r'nutrition/', include('match.nutrition.urls')),
    (r'^_stats/$', TemplateView.as_view(template_name="main/stats.html")),
    (r'^ce-credit-confirmation/', 'match.main.views.ce_credit_confirmation'),
    (r'^instructor/(?P<path>.*)$', 'match.main.views.instructor_page'),

    (r'^(?P<hierarchy>[\w\-]+)/edit/(?P<path>.*)$',
     'match.main.views.edit_page'),

    (r'^module_one/(?P<path>.+)$', 'match.main.views.module_one'),

    (r'^module_two/(?P<path>.+)$', 'match.main.views.module_two'),

    (r'^module_three/speechpathology/glossary/',
     'match.main.views.module_three_glossary'),
    (r'^module_three/(?P<path>.+)$', 'match.main.views.module_three'),

    (r'^module_four/(?P<path>.+)$', 'match.main.views.module_four'),

    (r'^module_five/(?P<path>.+)$', 'match.main.views.module_five'),
)
