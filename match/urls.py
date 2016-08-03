import django.contrib.auth.views
import django.views.static
import djangowind.views
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from match.main.views import (
    intro, background, all_results, all_results_key,
    ce_credit_confirmation, instructor_page, module_one,
    module_two, module_three, module_three_glossary, module_four,
    module_five, edit_page
)

admin.autodiscover()

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)

auth_urls = url(r'^accounts/', include('django.contrib.auth.urls'))

logout_page = url(r'^accounts/logout/$', django.contrib.auth.views.logout,
                  {'next_page': redirect_after_logout})
admin_logout_page = url(r'^accounts/logout/$',
                        django.contrib.auth.views.logout,
                        {'next_page': '/admin/'})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = url(r'^accounts/', include('djangowind.urls'))
    logout_page = url(r'^accounts/logout/$', djangowind.views.logout,
                      {'next_page': redirect_after_logout})
    admin_logout_page = url(r'^admin/logout/$', djangowind.views.logout,
                            {'next_page': redirect_after_logout})

urlpatterns = [
    logout_page,
    admin_logout_page,
    auth_urls,
    url(r'^$', intro),
    url(r'^intro/$', intro),
    url(r'^about/$', background, {'content_to_show': 'about'}),
    url(r'^help/$', background, {'content_to_show': 'help'}),
    url('^admin/allresults/$', all_results),
    url('^admin/allresultskey/$', all_results_key),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registration/', include('registration.urls')),
    url(r'^smoketest/', include('smoketest.urls')),
    url(r'^pagetree/', include('pagetree.urls')),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^_quiz/', include('quizblock.urls')),
    url(r'^_careermap/', include('careermapblock.urls')),
    url(r'nutrition/', include('match.nutrition.urls')),
    url(r'^_stats/$', TemplateView.as_view(template_name="main/stats.html")),
    url(r'^ce-credit-confirmation/', ce_credit_confirmation),
    url(r'^instructor/(?P<path>.*)$', instructor_page),

    url(r'^(?P<hierarchy>[\w\-]+)/edit/(?P<path>.*)$', edit_page),

    url(r'^module_one/(?P<path>.+)$', module_one),

    url(r'^module_two/(?P<path>.+)$', module_two),

    url(r'^module_three/speechpathology/glossary/', module_three_glossary),
    url(r'^module_three/(?P<path>.+)$', module_three),

    url(r'^module_four/(?P<path>.+)$', module_four),

    url(r'^module_five/(?P<path>.+)$', module_five),
]
