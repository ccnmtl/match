from django.db import models
from django.contrib.auth.models import User
from pagetree.models import PageBlock, Section
from django import forms
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name="application_user")
    last_location = models.CharField(max_length=255,default="/")

    def __unicode__(self):
        return self.user.username
    
    def display_name(self):
        return self.user.username
        

class UserVisited(models.Model):
    user = models.ForeignKey(UserProfile)
    section = models.ForeignKey(Section)
    visited_time = models.DateTimeField(auto_now=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance,last_location="/")

post_save.connect(create_user_profile, sender=User)
