from django import forms
from django.db import models
from django.contrib.auth.models import User
from pagetree.models import Section, PageBlock
from django.contrib.contenttypes import generic


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    last_location = models.CharField(max_length=255, default="/")

    def __unicode__(self):
        return self.user.username

    def display_name(self):
        return self.user.username

    def save_visit(self, section):
        self.last_location = section.get_absolute_url()
        self.save()
        uv, created = UserVisited.objects.get_or_create(
            user=self, section=section)

    def save_visits(self, sections):
        for s in sections:
            self.save_visit(s)

    def has_visited(self, section):
        return UserVisited.objects.filter(
            user=self, section=section).count() > 0


class UserVisited(models.Model):
    def __unicode__(self):
        return "%s visited %s" % (self.user, self.section.label)

    user = models.ForeignKey(UserProfile)
    section = models.ForeignKey(Section)
    visited_time = models.DateTimeField(auto_now=True)


class GlossaryTerm(models.Model):
    term = models.CharField(max_length=255)
    definition = models.TextField()

    def slug(self):
        return

    def __unicode__(self):
        return "%s - %s" % (self.term, self.definition)


class ImageMapItem(models.Model):
    label_name = models.CharField(max_length=64, default='')
    label = models.CharField(max_length=64)
    content = models.TextField()
    map_area_shape = models.CharField(max_length=64, default='')
    coordinates = models.TextField()

    def __unicode__(self):
        return self.label_name


class ImageMapChart(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "main/imagemapchart.html"
    js_template_file = "main/imagemapchart_js.html"
    css_template_file = "main/imagemapchart_css.html"
    display_name = "Interactive Image Map Chart"
    intro_text = models.TextField(default='')

    items = models.ManyToManyField(ImageMapItem)

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return ImageMapChartForm()

    def edit_form(self):
        return ImageMapChartForm(instance=self)

    @classmethod
    def create(self, request):
        form = ImageMapChartForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = ImageMapChartForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True


class ImageMapChartForm(forms.ModelForm):
    class Meta:
        model = ImageMapChart
        exclude = []
