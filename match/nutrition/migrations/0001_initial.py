# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CounselingReferral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_chart', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CounselingReferralState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('referral_date', models.DateField(auto_now_add=True)),
                ('referred_to', models.CharField(max_length=512, null=True, blank=True)),
                ('referred_from', models.CharField(max_length=512, null=True, blank=True)),
                ('reason', models.TextField(null=True, blank=True)),
                ('medical_history', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(related_name='nutrition_referral_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CounselingSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('available_time', models.IntegerField(default=0)),
                ('patient_chart', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CounselingSessionState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('elapsed_time', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DiscussionTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('estimated_time', models.IntegerField()),
                ('reply', models.TextField()),
                ('actual_time', models.IntegerField()),
                ('summary_text', models.TextField()),
                ('summary_reply', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='counselingsessionstate',
            name='answered',
            field=models.ManyToManyField(to='nutrition.DiscussionTopic', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='counselingsessionstate',
            name='session',
            field=models.ForeignKey(to='nutrition.CounselingSession'),
        ),
        migrations.AddField(
            model_name='counselingsessionstate',
            name='user',
            field=models.ForeignKey(related_name='nutrition_discussion_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='counselingsession',
            name='topics',
            field=models.ManyToManyField(to='nutrition.DiscussionTopic'),
        ),
    ]
