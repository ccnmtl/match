# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pagetree', '0002_delete_testblock'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GlossaryTerm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=255)),
                ('definition', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ImageMapChart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('intro_text', models.TextField(default=b'')),
            ],
        ),
        migrations.CreateModel(
            name='ImageMapItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label_name', models.CharField(default=b'', max_length=64)),
                ('label', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('map_area_shape', models.CharField(default=b'', max_length=64)),
                ('coordinates', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_location', models.CharField(default=b'/', max_length=255)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserVisited',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visited_time', models.DateTimeField(auto_now=True)),
                ('section', models.ForeignKey(to='pagetree.Section')),
                ('user', models.ForeignKey(to='main.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='imagemapchart',
            name='items',
            field=models.ManyToManyField(to='main.ImageMapItem'),
        ),
    ]
