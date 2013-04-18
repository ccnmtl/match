from django.test import TestCase
from match.main.models import GlossaryTerm


class SimpleTest(TestCase):
    def setUp(self):
        self.gt = GlossaryTerm.objects.create(
            term="foo",
            definition="bar")

    def tearDown(self):
        self.gt.delete()

    def test_unicode(self):
        self.assertEquals(unicode(self.gt), "foo - bar")
