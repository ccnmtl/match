from django.test import TestCase
from match.nutrition.models import DiscussionTopic


class SimpleTest(TestCase):
    def setUp(self):
        self.dt = DiscussionTopic.objects.create(
            text="some text",
            estimated_time=5,
            reply="a reply",
            actual_time=10,
            summary_text="summary text",
            summary_reply="summary reply")

    def tearDown(self):
        self.dt.delete()

    def test_unicode(self):
        self.assertEquals(
            unicode(self.dt.text),
            "some text")
