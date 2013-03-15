from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()
from django.views.generic.simple import direct_to_template

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = patterns(
    '',
    (r'^$', 'match.main.views.intro'),
    (r'^intro/$', 'match.main.views.intro'),
    (r'^about/$', 'match.main.views.background', {'content_to_show': 'about'}),
    (r'^help/$', 'match.main.views.background', {'content_to_show': 'help'}),
    ('^admin/allresults/$', 'match.main.views.all_results'),
    ('^admin/allresultskey/$', 'match.main.views.all_results_key'),
    (r'^admin/pagetree/', include('pagetree.urls')),
    (r'^admin/quiz/', include('quizblock.urls')),
    (r'^admin/', include(admin.site.urls)),
    ('^accounts/', include('djangowind.urls')),
    (r'^registration/', include('registration.urls')),
    (r'^munin/', include('munin.urls')),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^_quiz/', include('quizblock.urls')),
    (r'^_careermap/', include('careermapblock.urls')),
    (r'nutrition/', include('match.nutrition.urls')),
    (r'^_stats/', direct_to_template, {'template': 'main/stats.html'}),
    (r'^ce-credit-confirmation/', 'match.main.views.ce_credit_confirmation'),
    (r'^instructor/(?P<path>.*)$', 'match.main.views.instructor_page'),
    (r'^edit/(?P<path>.*)$', 'match.main.views.edit_page', {}, 'edit-page'),

    (r'^module_one/(?P<path>.+)$', 'match.main.views.module_one'),
    (r'^module_two/(?P<path>.+)$', 'match.main.views.module_two'),
    (r'^module_three/(?P<path>.+)$', 'match.main.views.module_three'),
    (r'^module_four/(?P<path>.+)$', 'match.main.views.module_four'),
    (r'^module_five/(?P<path>.+)$', 'match.main.views.module_five'),
)
