from django.contrib.auth.models import User
from match.main.models import UserProfile
from pagetree.models import Hierarchy, Section
import factory


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: "user%03d" % n)
    is_staff = True


class UserProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(UserFactory)


class HierarchyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Hierarchy
    name = "main"
    base_url = ""


class RootSectionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Section
    hierarchy = factory.SubFactory(HierarchyFactory)
    label = "Root"
    slug = ""


class ModuleFactory(object):
    def __init__(self, hname):
        base_url = "/%s/" % hname
        h = HierarchyFactory(name=hname, base_url=base_url)
        root = h.get_root()
        root.add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        root.add_child_section_from_dict({'label': "Two", 'slug': "two"})
        self.root = root
