from django.test import TestCase
from django.test.client import Client


class SimpleViewTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index(self):
        # it should redirect us somewhere.
        response = self.c.get("/")
        self.assertEquals(response.status_code, 302)
        # for now, we don't care where. really, we
        # are just making sure it's not a 500 error
        # at this point
