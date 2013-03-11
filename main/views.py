from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse, \
    HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.utils.encoding import smart_str
from main.models import GlossaryTerm, UserProfile
from nutrition.models import CounselingSessionState, \
    CounselingReferralState, DiscussionTopic
from pagetree.helpers import get_section_from_path, \
    get_module, needs_submit, submitted
from pagetree.models import Hierarchy
from quizblock.models import Submission, Response
import csv
import django.core.exceptions


def get_or_create_profile(user, section):
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
    except django.core.exceptions.MultipleObjectsReturned:
        user_profile = UserProfile.objects.filter(user=user)[0]
        created = False
    if created:
        first_leaf = section.hierarchy.get_first_leaf(section)
        ancestors = first_leaf.get_ancestors()
        for a in ancestors:
            user_profile.save_visit(a)
    return user_profile


class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if isinstance(items, type({})):
                ctx = RequestContext(request)
                return render_to_response(self.template_name,
                                          items,
                                          context_instance=ctx)
            else:
                return items
        return rendered_func


def has_responses(section):
    quizzes = [p.block() for p in section.pageblock_set.all(
    ) if hasattr(p.block(), 'needs_submit') and p.block().needs_submit()]
    return quizzes != []


def allow_redo(section):
    """ if blocks on the page allow redo """
    allowed = True
    for p in section.pageblock_set.all():
        if hasattr(p.block(), 'allow_redo'):
            if not p.block().allow_redo:
                allowed = False
    return allowed


def _unlocked(profile, section):
    """ if the user can proceed past this section """
    if not section:
        return True
    if section.is_root():
        return True
    if profile.has_visited(section):
        return True

    previous = section.get_previous()
    if not previous:
        return True
    else:
        if not profile.has_visited(previous):
            return False

    # if the previous page had blocks to submit
    # we only let them by if they submitted
    for p in previous.pageblock_set.all():
        if hasattr(p.block(), 'unlocked'):
            if not p.block().unlocked(profile.user):
                return False

    return profile.has_visited(previous)


def background(request, content_to_show):
    """ the pagetree page view breaks flatpages,
        so this is a simple workaround."""
    file_names = {
        'about': 'about.html',
        # 'credits' : 'credits.html',
        # 'contact' : 'contact.html',
        'help': 'help.html',
    }

    if content_to_show not in file_names.keys():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    file_name = file_names[content_to_show]
    t = loader.get_template('standard_elements/%s' % file_name)
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))


@login_required
@rendered_with('main/intro.html')
def intro(request):
    return dict()


@login_required
@rendered_with('main/ce_credit_confirmation.html')
def ce_credit_confirmation(request):
    return dict()


def module_one(request, path):
    hierarchy = Hierarchy.objects.get(name="module_one")
    return page(request, hierarchy, path)


def module_two(request, path):
    hierarchy = Hierarchy.objects.get(name="module_two")
    return page(request, hierarchy, path)


def module_three(request, path):
    hierarchy = Hierarchy.objects.get(name="module_three")
    return page(request, hierarchy, path)


def module_four(request, path):
    hierarchy = Hierarchy.objects.get(name="module_four")
    return page(request, hierarchy, path)


def module_five(request, path):
    hierarchy = Hierarchy.objects.get(name="module_five")
    return page(request, hierarchy, path)


@login_required
@rendered_with('main/page.html')
def page(request, hierarchy, path):
    section = get_section_from_path(path, hierarchy=hierarchy.name)
    root = section.hierarchy.get_root()
    module = get_module(section)
    user_profile = get_or_create_profile(user=request.user, section=section)

    can_access = _unlocked(user_profile, section)
    if can_access:
        user_profile.save_visit(section)
    else:
        # need to redirect them back
        return HttpResponseRedirect(user_profile.last_location)

    can_edit = False
    if not request.user.is_anonymous():
        can_edit = request.user.is_staff

    if section.id == root.id or section.id == root.get_first_child().id:
        # trying to visit the root page -- send them to the first leaf
        first_leaf = section.hierarchy.get_first_leaf(section)
        ancestors = first_leaf.get_ancestors()

        user_profile.save_visits(ancestors)
        return HttpResponseRedirect(first_leaf.get_absolute_url())

    if request.method == "POST":
        # user has submitted a form. deal with it
        if request.POST.get('action', '') == 'reset':
            section.reset(request.user)
            return HttpResponseRedirect(section.get_absolute_url())

        proceed = section.submit(request.POST, request.user)

        # on certain pages, we want to provide feedback instead of
        # sending them to the next page
        feedback_paths = ("socialwork/what-would-you-do/the-family/",
                          "socialwork/myths/mythfact-question-1/",
                          "socialwork/myths/mythfact-question-2/",
                          "socialwork/myths/mythfact-question-3/",
                          "socialwork/myths/mythfact-question-4/",
                          )
        for fb in feedback_paths:
            if path.startswith(fb):
                return HttpResponseRedirect(section.get_absolute_url())

        if not proceed:
            return HttpResponseRedirect(section.get_absolute_url())
        else:
            return HttpResponseRedirect(section.get_next().get_absolute_url())
    else:
        instructor_link = has_responses(section)
        return dict(section=section,
                    module=module,
                    glossary=GlossaryTerm.objects.all(),
                    needs_submit=needs_submit(section),
                    is_submitted=submitted(section, request.user),
                    allow_redo=allow_redo(section),
                    modules=root.get_children(),
                    root=section.hierarchy.get_root(),
                    instructor_link=instructor_link,
                    can_edit=can_edit,
                    next_unlocked=_unlocked(user_profile, section.get_next())
                    )


@login_required
@rendered_with("main/instructor_page.html")
def instructor_page(request, path):
    hierarchy_name, slash, section_path = path.partition('/')
    section = get_section_from_path(section_path, hierarchy=hierarchy_name)

    root = section.hierarchy.get_root()

    if request.method == "POST":
        if 'clear' in request.POST.keys():
            submission = get_object_or_404(
                Submission, id=request.POST['clear'])
            submission.delete()
            path = "/instructor" + section.get_absolute_url()
            return HttpResponseRedirect(path)

    quizzes = [p.block() for p in section.pageblock_set.all(
    ) if hasattr(p.block(), 'needs_submit') and p.block().needs_submit()]
    return dict(section=section,
                quizzes=quizzes,
                module=get_module(section),
                modules=root.get_children(),
                root=root)


def clean_header(s):
    s = s.replace('<div class=\'question-sub\'>', '')
    s = s.replace('<div class=\'question\'>', '')
    s = s.replace('<div class=\"mf-question\">', '')
    s = s.replace('<div class=\"sw-question\">', '')
    s = s.replace('<p>', '')
    s = s.replace('</p>', '')
    s = s.replace('</div>', '')
    s = s.replace('\n', '')
    s = s.replace('\r', '')
    s = s.replace('<', '')
    s = s.replace('>', '')
    s = s.replace('\'', '')
    s = s.replace('\"', '')
    s = s.replace(',', '')
    s = s.encode('utf-8')
    return s


class Column(object):
    def __init__(self, hierarchy, question=None, answer=None,
                 session=None, topic=None, field=None):
        self.hierarchy = hierarchy
        self.question = question
        self.answer = answer
        self.topic = topic
        self.field = field
        self.session = session
        self.module_name = self.hierarchy.get_top_level()[0].label

        if self.question:
            self._submission_cache = Submission.objects.filter(
                quiz=self.question.quiz)
            self._response_cache = Response.objects.filter(
                question=self.question)
            self._answer_cache = self.question.answer_set.all()

    def question_id(self):
        return "%s_question_%s" % (self.hierarchy.id, self.question.id)

    def question_answer_id(self):
        return "%s_%s" % (self.question_id(), self.answer.id)

    def counseling_id(self):
        return "%s_counseling_%s" % (self.hierarchy.id, self.session.id)

    def counseling_topic_id(self):
        return "%s_counseling_%s_%s" % (self.hierarchy.id,
                                        self.session.id,
                                        self.topic.id)

    def referral_id(self):
        return "%s_referral_%s" % (self.hierarchy.id, self.field)

    def question_value(self, user):
        r = self._submission_cache.filter(user=user).order_by("-submitted")
        if r.count() == 0:
            # user has not submitted this form
            return ""
        submission = r[0]
        r = self._response_cache.filter(submission=submission)
        if r.count() > 0:
            if (self.question.is_short_text() or
                    self.question.is_long_text()):
                return r[0].value
            elif self.question.is_multiple_choice():
                if self.answer.value in [res.value for res in r]:
                    return self.answer.id
            else:  # single choice
                for a in self._answer_cache:
                    if a.value == r[0].value:
                        return a.id

        return ''

    def user_value(self, user):
        if self.question:
            return self.question_value(user)

        elif self.session and self.topic:
            state = CounselingSessionState.objects.filter(
                session=self.session, user=user)
            if len(state) > 0:
                try:
                    state[0].answered.get(id=self.topic.id)
                    return self.topic.id
                except DiscussionTopic.DoesNotExist:
                    pass
        elif self.field:
            referral = CounselingReferralState.objects.filter(user=user)
            if len(referral) > 0:
                val = getattr(referral[0], self.field)
                if val is not None:
                    return val

        return ''

    def key_row(self):
        if self.question:
            row = [self.question_id(
            ), self.module_name, self.question.question_type,
                clean_header(self.question.text)]
            if self.answer:
                row.append(self.answer.id)
                row.append(clean_header(self.answer.label))
            return row
        elif self.session and self.topic:
            row = [self.counseling_id(), self.module_name,
                   "multiple choice", "Nutrition Counseling Session"]
            row.append(self.topic.id)
            row.append(clean_header(self.topic.summary_text))
            return row
        elif self.session and self.field:
            return [self.referral_id(),
                    self.module_name,
                    "short text",
                    clean_header(self.field), '', ""]

    def header_column(self):
        if self.question and self.answer:
            return [self.question_answer_id()]
        elif self.question:
            return [self.question_id()]
        elif self.session and self.topic:
            return [self.counseling_topic_id()]
        elif self.session and self.field:
            return [self.referral_id()]


def _get_quiz_key(h, s):
    columns = []
    quiz_type = ContentType.objects.filter(name='quiz')

    # quizzes
    for p in s.pageblock_set.filter(content_type=quiz_type):
        for q in p.block().question_set.all():
            if q.answerable():
                # need to make a column for each answer
                for a in q.answer_set.all():
                    columns.append(
                        Column(hierarchy=h, question=q, answer=a))
            else:
                columns.append(Column(hierarchy=h, question=q))

    return columns


def _get_quiz_results(h, s):
    columns = []
    quiz_type = ContentType.objects.filter(name='quiz')
    # quizzes
    for p in s.pageblock_set.filter(content_type=quiz_type):
        for q in p.block().question_set.all():
            if q.answerable() and q.is_multiple_choice():
                # need to make a column for each answer
                for a in q.answer_set.all():
                    columns.append(
                        Column(hierarchy=h, question=q, answer=a))
            else:
                columns.append(Column(hierarchy=h, question=q))

    return columns


@login_required
def all_results_key(request):

    """
        A "key" for all questions and answers in the system.
        * One row for short/long text questions
        * Multiple rows for single/multiple-choice questions.
        Each question/answer pair get a row
        itemIdentifier - unique system identifier,
            concatenates hierarchy id, item type string,
            page block id (if necessary) and item id
        module - first child label in the hierarchy
        itemType - [question, discussion topic, referral field]
        itemText - identifying text for the item
        answerIdentifier - for single/multiple-choice questions. an answer id
        answerText
    """

    if not request.user.is_superuser:
        return HttpResponseForbidden

    response = HttpResponse(mimetype='text/csv')
    response[
        'Content-Disposition'] = 'attachment; filename=match_response_key.csv'
    writer = csv.writer(response)
    headers = ['itemIdentifier', 'module', 'itemType', 'itemText',
               'answerIdentifier', 'answerText']
    writer.writerow(headers)

    counseling_type = ContentType.objects.filter(name='counseling session')
    referral_type = ContentType.objects.filter(name='counseling referral')

    columns = []
    for h in Hierarchy.objects.all():
        for s in h.get_root().get_descendants():
            columns = columns + _get_quiz_key(h, s)

            for p in s.pageblock_set.filter(content_type=counseling_type):
                for t in p.block().topics.all():
                    columns.append(Column(
                        hierarchy=h, session=p.content_object, topic=t))

            for p in s.pageblock_set.filter(content_type=referral_type):
                for f in p.block().form_fields:
                    columns.append(Column(
                        hierarchy=h, session=p.content_object, field=f))

    for column in columns:
        try:
            writer.writerow(column.key_row())
        except:
            pass

    return response


@login_required
@rendered_with("main/all_results.html")
def all_results(request):
    """
        All system results
        * One or more column for each question in system.
            ** 1 column for short/long text. label = itemIdentifier from key
            ** 1 column for single choice. label = itemIdentifier from key
            ** n columns for multiple choice: 1 column for each possible answer
               *** column labeled as itemIdentifer_answer.id

        * One row for each user in the system.
            1. username
            2 - n: answers
                * short/long text. text value
                * single choice. answer.id
                * multiple choice.
                    ** answer id is listed in each question/answer
                    column the user selected
                * Unanswered fields represented as an empty cell
    """

    if not request.user.is_superuser:
        return HttpResponseForbidden

    if not request.GET.get('format', 'html') == 'csv':
        return dict()

    counseling_type = ContentType.objects.filter(name='counseling session')
    referral_type = ContentType.objects.filter(name='counseling referral')

    columns = []
    for h in Hierarchy.objects.all():
        for s in h.get_root().get_descendants():
            columns = columns + _get_quiz_results(h, s)

            for p in s.pageblock_set.filter(content_type=counseling_type):
                for t in p.block().topics.all():
                    columns.append(Column(
                        hierarchy=h, session=p.content_object, topic=t))

            for p in s.pageblock_set.filter(content_type=referral_type):
                for f in p.block().form_fields:
                    columns.append(Column(
                        hierarchy=h, session=p.content_object, field=f))

    response = HttpResponse(mimetype='text/csv')
    response[
        'Content-Disposition'] = 'attachment; filename=match_responses.csv'
    writer = csv.writer(response)

    headers = ['userIdentifier']
    for c in columns:
        headers += c.header_column()
    writer.writerow(headers)

    # Only look at users who have submission
    users = User.objects.filter(submission__isnull=False).distinct()
    for u in users:
        row = [u.username]
        for column in columns:
            v = smart_str(column.user_value(u))
            row.append(v)

        writer.writerow(row)

    return response


@login_required
@rendered_with('main/edit_page.html')
def edit_page(request, path):
    hierarchy_name, slash, section_path = path.partition('/')
    section = get_section_from_path(section_path, hierarchy=hierarchy_name)

    root = section.hierarchy.get_root()

    return dict(section=section,
                module=get_module(section),
                modules=root.get_children(),
                root=root)
