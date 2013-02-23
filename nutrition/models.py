from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db import models
from pagetree.models import PageBlock
import time


class DiscussionTopic(models.Model):
    def __unicode__(self):
        if self.text and len(self.text) > 25:
            return self.text[:25] + '...'
        else:
            self.text

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
    css_template_file = "nutrition/nutrition_css.html"
    display_name = "Activity: Nutrition Counseling"

    topics = models.ManyToManyField(DiscussionTopic)
    available_time = models.IntegerField(default=0)
    patient_chart = models.TextField(null=True, blank=True)

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
        for topic in self.topics.all():
            if topic.estimated_time <= available_time:
                try:
                    state.answered.get(id=topic.id)
                except DiscussionTopic.DoesNotExist:
                    return False

        return True


class CounselingSessionForm(forms.ModelForm):
    class Meta:
        model = CounselingSession


class CounselingReferral(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "nutrition/referral.html"
    js_template_file = "nutrition/referral_js.html"
    css_template_file = "nutrition/nutrition_css.html"
    display_name = "Activity: Nutrition Counseling Referral"
    allow_redo = False
    patient_chart = models.TextField(null=True, blank=True)
    form_fields = ['referral_date', 'referred_to', 'referred_from',
                   'reason', 'medical_history']

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return True

    def submit(self, user, data):
        referral, created = CounselingReferralState.objects.get_or_create(
            user=user)

        for k in data.keys():
            value = data[k].strip()
            if k == 'referral_date':
                tm_struct = time.strptime(data[k], '%m/%d/%Y')
                value = time.strftime('%Y-%m-%d', tm_struct)

            referral.__setattr__(k, value)

        referral.save()

    def redirect_to_self_on_submit(self):
        return True

    @classmethod
    def add_form(self):
        return CounselingReferralForm()

    def edit_form(self):
        return CounselingReferralForm(instance=self)

    @classmethod
    def create(self, request):
        form = CounselingReferralForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = CounselingReferralForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        '''
            This module is unlocked if:
            1. The user has submitted a valid referral
        '''
        a = CounselingReferralState.objects.filter(user=user)
        if len(a) < 1:
            return False

        return a[0].is_complete()


class CounselingReferralForm(forms.ModelForm):
    class Meta:
        model = CounselingReferral


class CounselingSessionState(models.Model):
    def __unicode__(self):
        return "%s -- %s" % (self.user.username, self.session)

    user = models.ForeignKey(User, related_name="nutrition_discussion_user")
    session = models.ForeignKey(CounselingSession)
    answered = models.ManyToManyField(DiscussionTopic, null=True, blank=True)
    elapsed_time = models.IntegerField(default=0)


class CounselingReferralState(models.Model):
    def __unicode__(self):
        return "%s" % (self.user.username)

    user = models.ForeignKey(User, related_name="nutrition_referral_user")
    referral_date = models.DateField(auto_now_add=True)
    referred_to = models.CharField(max_length=512, null=True, blank=True)
    referred_from = models.CharField(max_length=512, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)

    def is_complete(self):
        return self.referred_to is not None and \
            self.referred_from is not None and \
            self.reason is not None and \
            self.medical_history is not None and \
            len(self.referred_to) > 0 and \
            len(self.referred_from) > 0 and \
            len(self.reason) > 0 and \
            len(self.medical_history) > 0
