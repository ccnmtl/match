from django.conf.urls import include, url
from match.nutrition.api import CounselingSessionResource, \
    CounselingSessionStateResource, DiscussionTopicResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(DiscussionTopicResource())
v1_api.register(CounselingSessionResource())
v1_api.register(CounselingSessionStateResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
]
