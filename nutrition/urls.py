from django.conf.urls.defaults import *
import os.path
from tastypie.api import Api
from nutrition.api import UserResource, DiscussionResponseResource, DiscussionTopicResource
from nutrition.api import CounselingSessionResource, CounselingSessionStateResource

media_root = os.path.join(os.path.dirname(__file__),"media")

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(DiscussionResponseResource())
v1_api.register(DiscussionTopicResource())
v1_api.register(CounselingSessionResource())
v1_api.register(CounselingSessionStateResource())

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
    (r'^api/', include(v1_api.urls)),

    #(r'^load/$', 'match.nutrition.views.loadstate'),
    #(r'^save/$', 'match.nutrition.views.savestate')
)