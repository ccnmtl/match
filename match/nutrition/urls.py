import django.views.static
import os.path
from django.conf.urls import include, url
from match.nutrition.api import CounselingSessionResource, \
    CounselingSessionStateResource, DiscussionTopicResource
from tastypie.api import Api

media_root = os.path.join(os.path.dirname(__file__), "media")

v1_api = Api(api_name='v1')
v1_api.register(DiscussionTopicResource())
v1_api.register(CounselingSessionResource())
v1_api.register(CounselingSessionStateResource())

urlpatterns = [
    url(r'^media/(?P<path>.*)$', django.views.static.serve, {
        'document_root': media_root}),
    url(r'^api/', include(v1_api.urls)),
]
