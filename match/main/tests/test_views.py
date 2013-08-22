from django.test import TestCase
from django.test.client import Client
from .factories import UserProfileFactory, ModuleFactory
from match.main.views import Column, clean_header


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

    def test_smoke(self):
        # run the smoketests. we don't care if they pass
        # or fail, we just want to make sure that the
        # smoketests themselves don't have an error
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)


class LoggedInViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.up = UserProfileFactory()
        self.user = self.up.user
        self.user.set_password("test")
        self.user.save()
        self.c.login(username=self.user.username, password="test")

    def test_index(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_ce_credit_confirmation(self):
        response = self.c.get("/ce-credit-confirmation/")
        self.assertEquals(response.status_code, 200)

    def test_module_one_page(self):
        ModuleFactory("module_one")
        # need to visit the module page first in order to be allowed
        # access to the intro page
        response = self.c.get("/module_one/socialwork/")
        response = self.c.get("/module_one/socialwork/introduction/")
        self.assertEquals(response.status_code, 200)

    def test_module_one_page_post(self):
        ModuleFactory("module_one")
        response = self.c.get("/module_one/socialwork/")
        response = self.c.get("/module_one/socialwork/introduction/")
        self.assertEquals(response.status_code, 200)
        response = self.c.post("/module_one/socialwork/introduction/")
        self.assertEqual(response.status_code, 302)
        response = self.c.post("/module_one/socialwork/introduction/",
                               dict(action='reset'))
        self.assertEqual(response.status_code, 302)

    def test_edit_page(self):
        ModuleFactory("module_one")
        response = self.c.get("/edit/module_one/socialwork/introduction/")
        self.assertEquals(response.status_code, 200)

    def test_instructor_page(self):
        ModuleFactory("module_one")
        response = self.c.get(
            "/instructor/module_one/socialwork/introduction/")
        self.assertEquals(response.status_code, 200)
        response = self.c.post(
            "/instructor/module_one/socialwork/introduction/")
        self.assertEquals(response.status_code, 200)

    def test_module_two_page(self):
        ModuleFactory("module_two")
        response = self.c.get("/module_two/socialwork/")
        response = self.c.get("/module_two/socialwork/introduction/")
        self.assertEquals(response.status_code, 200)

    def test_module_three_page(self):
        ModuleFactory("module_three")
        response = self.c.get("/module_three/socialwork/")
        response = self.c.get("/module_three/socialwork/introduction/")
        self.assertEquals(response.status_code, 200)

    def test_module_three_glossary(self):
        ModuleFactory("module_three")
        self.c.get("/module_three/speechpathology/glossary/")

    def test_module_four_page(self):
        ModuleFactory("module_four")
        response = self.c.get("/module_four/socialwork/")
        response = self.c.get("/module_four/socialwork/introduction/")
        self.assertEquals(response.status_code, 200)

    def test_module_five_page(self):
        ModuleFactory("module_five")
        response = self.c.get("/module_five/socialwork/")
        response = self.c.get("/module_five/socialwork/introduction/")
        self.assertEquals(response.status_code, 200)

    def test_allresults_key(self):
        ModuleFactory("module_one")
        # not a superuser
        response = self.c.get("/admin/allresultskey/")
        self.assertEquals(response.status_code, 403)
        self.user.is_superuser = True
        self.user.save()
        response = self.c.get("/admin/allresultskey/")
        self.assertEquals(response.status_code, 200)

    def test_allresults(self):
        ModuleFactory("module_one")
        # not a superuser
        response = self.c.get("/admin/allresults/")
        self.assertEquals(response.status_code, 403)
        self.user.is_superuser = True
        self.user.save()
        response = self.c.get("/admin/allresults/")
        self.assertEquals(response.status_code, 200)
        response = self.c.get("/admin/allresults/?format=csv")
        self.assertEquals(response.status_code, 200)


class ColumnTest(TestCase):
    def test_create(self):
        m = ModuleFactory("module_one")
        c = Column(m.root.hierarchy)
        self.assertEqual(c.module_name, "One")

    def test_header_column(self):
        m = ModuleFactory("module_one")
        c = Column(m.root.hierarchy)
        self.assertEqual(c.header_column(), None)

    def test_user_value(self):
        m = ModuleFactory("module_one")
        c = Column(m.root.hierarchy)
        self.assertEqual(c.user_value(None), '')

    def test_key_row(self):
        m = ModuleFactory("module_one")
        c = Column(m.root.hierarchy)
        self.assertEqual(c.key_row(), None)


class CleanHeaderTest(TestCase):
    def test_empty(self):
        self.assertEqual(clean_header(''), '')

    def test_markup(self):
        self.assertEqual(clean_header('<<<<foo>>>>'), 'foo')
