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
    summary_text = models.TextField()
    summary_reply = models.TextField()

class CounselingSession(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "nutrition/counseling.html"
    js_template_file = "nutrition/counseling_js.html"
    css_template_file = "nutrition/counseling_css.html"
    display_name = "Activity: Nutrition Counseling"

    topics = models.ManyToManyField(DiscussionTopic)
    available_time = models.IntegerField(default=0)
    patient_chart = models.TextField()

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
        '''
            This module is unlocked if:
            1. The available time <= 0
            2. All topics are discussed
            3. Undiscussed topics estimated_time > available_time
        '''
        a = CounselingSessionState.objects.filter(session=self, user=user)
        if len(a) < 1:
            return False

        state = a[0]
        available_time = self.available_time - state.elapsed_time

        if available_time <= 0:
            return True


        # All questions answered || unanswered questions are > available_time
        not_yet_discussed = 0
        for topic in self.topics.all():
            if topic.estimated_time <= available_time:
                try:
                    obj = state.answered.get(id=topic.id)
                except DiscussionTopic.DoesNotExist:
                    return False

        return True


class CounselingSessionState(models.Model):
    user = models.ForeignKey(User, related_name="nutrition_discussion_user")
    session = models.ForeignKey(CounselingSession)
    answered = models.ManyToManyField(DiscussionTopic, null=True, blank=True)
    elapsed_time = models.IntegerField(default=0)

class CounselingSessionForm(forms.ModelForm):
    class Meta:
        model = CounselingSession