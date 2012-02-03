from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()
from django.views.generic.simple import direct_to_template

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       (r'^about/',direct_to_template, {'template': 'main/about.html'}),
                       (r'^help/',direct_to_template, {'template': 'main/help.html'}),

                       (r'^export/$','main.views.exporter'),
                       (r'^import/$','main.views.importer'),

                       ('^_allresults/$','main.views.all_results'),
                       ('^accounts/',include('djangowind.urls')),
                       (r'^registration/', include('registration.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^munin/',include('munin.urls')),
                       (r'^pagetree/',include('pagetree.urls')),
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
                       (r'^_quiz/',include('quizblock.urls')),
                       (r'^_careermap/',include('careermapblock.urls')),
                       (r'^ce-credit-confirmation/','main.views.ce_credit_confirmation'),
                       (r'^edit/(?P<path>.*)$','match.main.views.edit_page',{},'edit-page'),
                       (r'^instructor/(?P<path>.*)$','match.main.views.instructor_page'),
                       (r'^(?P<path>.*)$','match.main.views.page'),
                       
) 

