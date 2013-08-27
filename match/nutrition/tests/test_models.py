from django.test import TestCase
from django.contrib.auth.models import User
from match.nutrition.models import DiscussionTopic, CounselingSession
from match.nutrition.models import CounselingSessionState
from match.nutrition.models import CounselingReferralState
from match.nutrition.models import CounselingReferral


class SimpleTest(TestCase):
    def test_unicode(self):
        dt = DiscussionTopic.objects.create(
            text='what about this?',
            estimated_time=5,
            reply="a reply",
            actual_time=10,
            summary_text="summary text",
            summary_reply="summary reply")
        self.assertEquals(
            str(dt),
            "what about this?")
        dt = DiscussionTopic.objects.create(
            text='',
            estimated_time=5,
            reply="a reply",
            actual_time=10,
            summary_text="summary text",
            summary_reply="summary reply")
        self.assertEquals(
            str(dt),
            "")

    def test_unicode_long_text(self):
        dt = DiscussionTopic.objects.create(
            text=''.join(str(x) for x in range(25)),
            estimated_time=5,
            reply="a reply",
            actual_time=10,
            summary_text="summary text",
            summary_reply="summary reply")
        self.assertEquals(
            unicode(dt),
            u'0123456789101112131415161...')


class CounselingSessionTest(TestCase):
    def test_needs_submit(self):
        cs = CounselingSession.objects.create()
        self.assertFalse(cs.needs_submit())

    def test_add_form(self):
        f = CounselingSession.add_form()
        self.assertTrue('topics' in f.fields)

    def test_edit_form(self):
        cs = CounselingSession.objects.create()
        f = cs.edit_form()
        self.assertTrue('topics' in f.fields)

    def test_unlocked(self):
        u = User.objects.create(username="testuser")
        cs = CounselingSession.objects.create()
        self.assertFalse(cs.unlocked(u))
        CounselingSessionState.objects.create(user=u, session=cs)
        self.assertTrue(cs.unlocked(u))


class CounselingReferralStateTest(TestCase):
    def test_unicode(self):
        u = User.objects.create(username="testuser")
        crs = CounselingReferralState(user=u)
        self.assertEqual(str(crs), "testuser")

    def test_is_complete(self):
        u = User.objects.create(username="testuser")
        crs = CounselingReferralState(user=u)
        self.assertFalse(crs.is_complete())


class CounselingReferralTest(TestCase):
    def test_needs_submit(self):
        cr = CounselingReferral.objects.create()
        self.assertTrue(cr.needs_submit())

    def test_redirect_to_self_on_submit(self):
        cr = CounselingReferral.objects.create()
        self.assertTrue(cr.redirect_to_self_on_submit())

    def test_edit_form(self):
        cr = CounselingReferral.objects.create()
        f = cr.edit_form()
        self.assertTrue(hasattr(f, 'fields'))

    def test_submit(self):
        cr = CounselingReferral.objects.create()
        u = User.objects.create(username="testuser")
        self.assertFalse(cr.unlocked(u))
        cr.submit(u, dict(referral_date='01/01/2001',
                          medical_history="patient is deceased"))
        self.assertEqual(
            CounselingReferralState.objects.filter(user=u).count(),
            1)
