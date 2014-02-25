from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from match.nutrition.models import DiscussionTopic, CounselingSession, \
    CounselingSessionState
from tastypie.authorization import Authorization


class UsernameAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        if bundle.request and hasattr(bundle.request, 'user'):
            return object_list.filter(username=bundle.request.user.username)

        return object_list.none()


class UserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        if bundle.request and hasattr(bundle.request, 'user'):
            return object_list.filter(user=bundle.request.user)

        return object_list.none()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff',
                    'is_superuser', 'date_joined']
        allowed_methods = ['get']
        authorization = UsernameAuthorization()


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
    answered = fields.ManyToManyField(
        'match.nutrition.api.DiscussionTopicResource', 'answered', full=False)

    class Meta:
        queryset = CounselingSessionState.objects.all()
        resource_name = 'counseling_session_state'
        allowed_methods = ['get', 'put']
        authorization = UserAuthorization()
