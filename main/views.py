from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from pagetree.helpers import get_hierarchy, get_section_from_path, get_module, needs_submit, submitted
from pagetree.models import Hierarchy
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from models import *
from quizblock.models import Submission, Response
from main.models import UserProfile
import csv
import django.core.exceptions

def get_or_create_profile(user,section):
    try:
        user_profile,created = UserProfile.objects.get_or_create(user=user)
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
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items
        return rendered_func

def has_responses(section):
    quizzes = [p.block() for p in section.pageblock_set.all() if hasattr(p.block(),'needs_submit') and p.block().needs_submit()]
    return quizzes != []


def allow_redo(section):
    """ if blocks on the page allow redo """
    allowed = True
    for p in section.pageblock_set.all():
        if hasattr(p.block(),'allow_redo'):
            if not p.block().allow_redo:
                allowed = False
    return allowed


def _unlocked(profile,section):
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
        if hasattr(p.block(),'unlocked'):
            if not p.block().unlocked(profile.user):
                return False
          
    return profile.has_visited(previous)

def background(request,  content_to_show):
    """ the pagetree page view breaks flatpages, so this is a simple workaround."""
    file_names = {
        'about'   : 'about.html',
        #'credits' : 'credits.html',
        #'contact' : 'contact.html',
        'help'    : 'help.html',
    } 

    if content_to_show not in file_names.keys():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    file_name = file_names [content_to_show]
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

@login_required
@rendered_with('main/page.html')
def page(request,path):
    hierarchy_name,slash,section_path = path.partition('/')
    section = get_section_from_path(section_path,hierarchy=hierarchy_name)

    root = section.hierarchy.get_root()
    module = get_module(section)

    user_profile = get_or_create_profile(user=request.user,section=section)

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
        if request.POST.get('action','') == 'reset':
            section.reset(request.user)
            return HttpResponseRedirect(section.get_absolute_url())

        proceed = section.submit(request.POST,request.user)

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
                    needs_submit=needs_submit(section),
                    is_submitted=submitted(section,request.user),
                    allow_redo=allow_redo(section),
                    modules=root.get_children(),
                    root=section.hierarchy.get_root(),
                    instructor_link=instructor_link,
                    can_edit=can_edit,
                    next_unlocked = _unlocked(user_profile,section.get_next())
                    )
@login_required
@rendered_with("main/instructor_page.html")
def instructor_page(request,path):
    hierarchy_name,slash,section_path = path.partition('/')
    section = get_section_from_path(section_path,hierarchy=hierarchy_name)

    root = section.hierarchy.get_root()

    if request.method == "POST":
        if 'clear' in request.POST.keys():
            submission = get_object_or_404(Submission,id=request.POST['clear'])
            submission.delete()
            return HttpResponseRedirect("/instructor" + section.get_absolute_url())

    quizzes = [p.block() for p in section.pageblock_set.all() if hasattr(p.block(),'needs_submit') and p.block().needs_submit()]
    return dict(section=section,
                quizzes=quizzes,
                module=get_module(section),
                modules=root.get_children(),
                root=root)

class Column(object):
    def __init__(self, hierarchy, question=None, answer=None):
        self.hierarchy = hierarchy
        self.question = question
        self.answer = answer
        self._submission_cache = Submission.objects.filter(quiz=self.question.quiz)
        self._response_cache = Response.objects.filter(question=self.question)


    def value(self, user):
        r = self._submission_cache.filter(user=user).order_by("-submitted")
        if r.count() == 0:
            # user has not submitted this form
            return ""
        submission = r[0]
        r = self._response_cache.filter(submission=submission)
        if r.count() > 0:
            if self.answer is None:
                # text/short answer type question
                return r[0].value
            else:
                # multiple/single choice
                if self.answer.value in [res.value for res in self.question.user_responses(user)]:
                    return self.answer.id
                else:
                    return ""
        else:
            # user submitted this form, but left this question blank somehow
            return ""

    def header_column(self):
        if self.answer:
            return [ "question_%s_%s" % (self.question.id, self.answer.id)]
        else:
            return [ "question_%s" % self.question.id ]


#def backup_to_csv(request):
#
#    output = StringIO.StringIO() ## temp output file
#    writer = csv.writer(output, dialect='excel')
#
#    #code for writing csv file go here...
#
#    response = HttpResponse(mimetype='application/zip')
#    response['Content-Disposition'] = 'attachment; filename=backup.csv.zip'
#
#    z = zipfile.ZipFile(response,'w')   ## write zip to response
#    z.writestr("filename.csv", output.getvalue())  ## write csv file to zip
#
#    return response

def clean_header(s):
    s = s.replace('<div class=\'question-sub\'>','')
    s = s.replace('<div class=\'question\'>','')
    s = s.replace('<div class=\'mf-question\'>','')
    s = s.replace('<div class=\'sw-question\'>','')
    s = s.replace('<p>','')
    s = s.replace('</p>','')
    s = s.replace('</div>','')
    s = s.replace('\n','')
    s = s.replace('\r','')
    s = s.replace('<','')
    s = s.replace('>','')
    s = s.replace('\'','')
    s = s.replace('\"','')
    s = s.replace(',','')
    s = s.encode('utf-8')
    return s

@login_required
def all_results_key(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=match_response_key.csv'
    writer = csv.writer(response)
    headers = ['module', 'questionIdentifier', 'questionType', 'questionText', 'answerIdentifier', 'answerText']
    writer.writerow(headers)

    for h in Hierarchy.objects.all():
        for s in h.get_root().get_descendants():
            for p in s.pageblock_set.all():
                if hasattr(p.block(),'needs_submit') and p.block().needs_submit():
                    for q in p.block().question_set.all():

                        answers = q.answer_set.all()

                        if len(answers) < 1:
                            try:
                                row = [h.name, q.id, q.question_type, clean_header(q.text)]
                                writer.writerow(row)
                            except:
                                pass
                        else:
                            for a in q.answer_set.all():
                                row = [h.name, q.id, q.question_type, clean_header(q.text), a.id, clean_header(a.label)]
                                try:
                                    writer.writerow(row)
                                except:
                                    pass

    return response


@login_required
@rendered_with("main/all_results.html")
def all_results(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden

    if not request.GET.get('format','html') == 'csv':
        return dict()

    columns = []
    for h in Hierarchy.objects.all():
        for s in h.get_root().get_descendants():
            for p in s.pageblock_set.all():
                if hasattr(p.block(),'needs_submit') and p.block().needs_submit():
                    for q in p.block().question_set.all():
                        if q.answerable():
                            # need to make a column for each answer
                            for a in q.answer_set.all():
                                columns.append(Column(hierarchy=h.name, question=q, answer=a))
                        else:
                            columns.append(Column(hierarchy=h.name, question=q))

    all_responses = []
    for u in User.objects.all():
        row = []
        for column in columns:
            v = column.value(u)
            row.append(v)
        all_responses.append(dict(user=u,row=row))


    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=match_responses.csv'
    writer = csv.writer(response)

    headers = ['userIdentifier']
    for c in columns:
        headers += c.header_column()
    writer.writerow(headers)

    for r in all_responses:
        # concatenate user name + all responses, iterate over and spit out a long csv string
        rd = [smart_str(c) for c in [r['user'].username] + r['row']]
        writer.writerow(rd)
    return response

@login_required
@rendered_with('main/edit_page.html')
def edit_page(request,path):
    hierarchy_name,slash,section_path = path.partition('/')
    section = get_section_from_path(section_path,hierarchy=hierarchy_name)

    root = section.hierarchy.get_root()

    return dict(section=section,
                module=get_module(section),
                modules=root.get_children(),
                root=section.hierarchy.get_root())


