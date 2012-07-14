from django.db import models
from django.utils import simplejson
from django.contrib.contenttypes import generic
from pagetree.models import PageBlock
from django import forms
from django.contrib.auth.models import User

class DiscussionTopic(models.Model):
    def __unicode__(self):
        return self.text[:25] + '...' if self.text and len(self.text) > 25 else self.text

    text = models.TextField()
    estimated_time = models.IntegerField()
    reply = models.TextField()
    actual_time = models.IntegerField()

class CounselingSession(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "nutrition/counseling.html"
    js_template_file = "nutrition/counseling_js.html"
    css_template_file = "nutrition/counseling_css.html"
    display_name = "Activity: Nutrition Counseling"

    topics = models.ManyToManyField(DiscussionTopic)
    available_time = models.IntegerField(default=0)

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return CounselingSessionForm()

    def edit_form(self):
        return CounselingSessionForm(instance=self)

    @classmethod
    def create(self, request):
        form = CounselingSessionForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = CounselingSessionForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        rc = False
        try:
            state = ActivityState.objects.get(user=user)
            obj = simplejson.loads(state.json)
            if obj.has_key('complete'):
                rc = obj['complete']
        except ActivityState.DoesNotExist:
            pass # ignore, we'll return false here in a sec

        return rc

class CounselingSessionState(models.Model):
    user = models.ForeignKey(User, related_name="nutrition_discussion_user")
    session = models.ForeignKey(CounselingSession)
    answered = models.ManyToManyField(DiscussionTopic, null=True, blank=True)
    elapsed_time = models.IntegerField(default=0)

class CounselingSessionForm(forms.ModelForm):
    class Meta:
        model = CounselingSession