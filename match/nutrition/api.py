from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from match.nutrition.models import DiscussionTopic, CounselingSession, \
    CounselingSessionState
from tastypie.authorization import Authorization


class UsernameAuthorization(Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(username=request.user.username)

        return object_list.none()


class UserAuthorization(Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(user=request.user)

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
        allowed_methods = ['get']


class CounselingSessionResource(ModelResource):
    topics = fields.ManyToManyField(
        'match.nutrition.api.DiscussionTopicResource', 'topics', full=True)

    class Meta:
        queryset = CounselingSession.objects.all()
        resource_name = 'counseling_session'
        allowed_methods = ['get']


class CounselingSessionStateResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    session = fields.ForeignKey(
        CounselingSessionResource, 'session', full=True)
    answered = fields.ManyToManyField(
        'match.nutrition.api.DiscussionTopicResource', 'answered', full=True)

    class Meta:
        queryset = CounselingSessionState.objects.all()
        resource_name = 'counseling_session_state'
        authorization = UserAuthorization()
        allowed_methods = ['get', 'put']
