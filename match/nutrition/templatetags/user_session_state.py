from django import template
from match.nutrition.models import CounselingSession, CounselingSessionState, \
    CounselingReferralState
register = template.Library()


class GetUserSessionState(template.Node):
    def __init__(self, user, session_id):
        self.user = template.Variable(user)
        self.session_id = template.Variable(session_id)

    def render(self, context):
        u = self.user.resolve(context)
        s = self.session_id.resolve(context)

        session = CounselingSession.objects.get(id=s)
        obj, create = CounselingSessionState.objects.get_or_create(
            user=u, session=session)
        return obj.id


@register.tag('get_user_session_state')
def get_user_session_state(parser, token):
    user = token.split_contents()[1:][0]
    session_id = token.split_contents()[1:][1]
    return GetUserSessionState(user, session_id)


class GetUserSessionStates(template.Node):
    def __init__(self, user):
        self.user = template.Variable(user)

    def render(self, context):
        u = self.user.resolve(context)
        context['user_session_states'] = CounselingSessionState.objects.filter(
            user=u)
        return ''


@register.tag('get_user_session_states')
def get_user_session_states(parser, token):
    user = token.split_contents()[1:][0]
    return GetUserSessionStates(user)


class GetPatientReferral(template.Node):
    def __init__(self, user):
        self.user = template.Variable(user)

    def render(self, context):
        u = self.user.resolve(context)

        obj, create = CounselingReferralState.objects.get_or_create(user=u)
        context['referral'] = obj
        return ''


@register.tag('get_patient_referral')
def get_patient_referral(parser, token):
    user = token.split_contents()[1:][0]
    return GetPatientReferral(user)
