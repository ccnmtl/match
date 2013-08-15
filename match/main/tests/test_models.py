from django.test import TestCase
from match.main.models import GlossaryTerm, ImageMapItem


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
