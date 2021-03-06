from django import template
from match.main.views import _unlocked

register = template.Library()


class UnlockedNode(template.Node):
    def __init__(self, section, nodelist_true, nodelist_false=None):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.section = section

    def render(self, context):
        s = context[self.section]
        r = context['request']
        u = r.user
        if _unlocked(u.profile, s):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.tag('ifunlocked')
def unlocked(parser, token):
    section = token.split_contents()[1:][0]
    nodelist_true = parser.parse(('else', 'endifunlocked'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifunlocked',))
        parser.delete_first_token()
    else:
        nodelist_false = None
    return UnlockedNode(section, nodelist_true, nodelist_false)


class SubmittedNode(template.Node):
    def __init__(self, section, nodelist_true, nodelist_false=None):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.section = section

    def render(self, context):
        if self.section not in context:
            return self.nodelist_false.render(context)

        s = context[self.section]
        r = context['request']
        u = r.user
        if s.submitted(u):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.tag('ifsubmitted')
def submitted(parser, token):
    section = token.split_contents()[1:][0]
    nodelist_true = parser.parse(('else', 'endifsubmitted'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifsubmitted',))
        parser.delete_first_token()
    else:
        nodelist_false = None
    return SubmittedNode(section, nodelist_true, nodelist_false)
