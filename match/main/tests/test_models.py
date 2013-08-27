from django.test import TestCase
from django.contrib.auth.models import User
from match.main.models import GlossaryTerm, ImageMapItem
from match.main.models import UserProfile, UserVisited
from match.main.models import ImageMapChart
from pagetree.models import Hierarchy


class GlossaryTermTest(TestCase):
    def test_unicode(self):
        gt = GlossaryTerm.objects.create(term="foo", definition="bar")
        self.assertEquals(unicode(gt), "foo - bar")

    def test_slug(self):
        gt = GlossaryTerm.objects.create(term="foo", definition="bar")
        self.assertEquals(gt.slug(), None)


class ImageMapItemTest(TestCase):
    def test_unicode(self):
        imi = ImageMapItem.objects.create(label="foo")
        self.assertEqual(str(imi), "")


class UserProfileTest(TestCase):
    def test_unicode(self):
        u = User.objects.create(username="testuser")
        up = UserProfile(user=u)
        self.assertEqual(str(up), "testuser")

    def test_displayname(self):
        u = User.objects.create(username="testuser")
        up = UserProfile(user=u)
        self.assertEqual(up.display_name(), "testuser")


class UserVisitedTest(TestCase):
    def test_unicode(self):
        h = Hierarchy.objects.create(name="main")
        u = User.objects.create(username="testuser")
        up = UserProfile(user=u)
        uv = UserVisited(user=up, section=h.get_root())
        self.assertEqual(str(uv), "testuser visited Root")


class ImageMapChartTest(TestCase):
    def test_needs_submit(self):
        imc = ImageMapChart.objects.create()
        self.assertFalse(imc.needs_submit())

    def test_edit_form(self):
        imc = ImageMapChart.objects.create()
        f = imc.edit_form()
        self.assertTrue("intro_text" in f.fields)

    def test_unlocked(self):
        imc = ImageMapChart.objects.create()
        self.assertTrue(imc.unlocked(None))
