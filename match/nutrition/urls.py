from django.conf.urls import patterns, include
from match.nutrition.api import CounselingSessionResource, \
    CounselingSessionStateResource, DiscussionTopicResource
from tastypie.api import Api
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

v1_api = Api(api_name='v1')
v1_api.register(DiscussionTopicResource())
v1_api.register(CounselingSessionResource())
v1_api.register(CounselingSessionStateResource())

urlpatterns = patterns(
    '',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
     'document_root': media_root}),
    (r'^api/', include(v1_api.urls)))
