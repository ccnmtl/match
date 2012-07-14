from django import template
from nutrition.models import CounselingSession, CounselingSessionState
register = template.Library()


class GetUserSessionState(template.Node):
    def __init__(self, user, session_id):
        self.user = template.Variable(user)
        self.session_id = template.Variable(session_id)

    def render(self, context):
        u = self.user.resolve(context)
        s = self.session_id.resolve(context)

        session = CounselingSession.objects.get(id=s)
        obj, create = CounselingSessionState.objects.get_or_create(user=u, session=session)
        return obj.id

@register.tag('get_user_session_state')
def get_user_session_state(parser, token):
    user = token.split_contents()[1:][0]
    session_id = token.split_contents()[1:][1]
    return GetUserSessionState(user, session_id)