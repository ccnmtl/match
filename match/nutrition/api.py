from tastypie import fields
from tastypie.resources import ModelResource
from match.nutrition.models import DiscussionTopic, CounselingSession, \
    CounselingSessionState
from tastypie.authorization import Authorization


class UserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        if bundle.request and hasattr(bundle.request, 'user'):
            return object_list.filter(user=bundle.request.user)

        return object_list.none()


class DiscussionTopicResource(ModelResource):
    class Meta:
        queryset = DiscussionTopic.objects.all()
        resource_name = 'discussion_topic'
        detail_allowed_methods = ['get']


class CounselingSessionResource(ModelResource):
    topics = fields.ManyToManyField(
        'match.nutrition.api.DiscussionTopicResource', 'topics',
        full=True, readonly=True)

    class Meta:
        queryset = CounselingSession.objects.all()
        resource_name = 'counseling_session'
        allowed_methods = ['get']


class CounselingSessionStateResource(ModelResource):
    session = fields.ForeignKey(
        CounselingSessionResource, 'session', full=True, readonly=True)
    answered = fields.ManyToManyField(
        'match.nutrition.api.DiscussionTopicResource', 'answered', full=False)

    class Meta:
        queryset = CounselingSessionState.objects.all()
        resource_name = 'counseling_session_state'
        allowed_methods = ['get', 'put']
        authorization = UserAuthorization()
