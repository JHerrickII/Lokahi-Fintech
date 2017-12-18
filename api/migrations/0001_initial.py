# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
from django.conf import settings
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('file', models.FileField(upload_to='tmp')),
            ],
        ),
        migrations.CreateModel(
            name='FullUserProfile',
            fields=[
                ('user', models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL)),
                ('user_type', models.CharField(max_length=200)),
                ('RSA_publickey', models.TextField(default='')),
                ('RSA_privatekey', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_encrypt', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1)),
                ('message_subject', models.CharField(max_length=2000)),
                ('message_body', models.CharField(max_length=2000)),
                ('message_from', models.CharField(max_length=200)),
                ('message_to', models.CharField(max_length=200)),
                ('message_delete', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1)),
                ('message_id', models.AutoField(serialize=False, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('report_name', models.CharField(max_length=200, default='')),
                ('report_files', models.FileField(upload_to='documents', null=True, blank=True)),
                ('company_name', models.CharField(max_length=50, default='')),
                ('company_phone', models.CharField(max_length=11, default='')),
                ('company_location', models.CharField(max_length=50, default='')),
                ('company_country', models.CharField(max_length=20, default='')),
                ('business_type', models.CharField(max_length=20, default='')),
                ('current_projects', models.TextField(max_length=100, default='')),
                ('private', models.BooleanField(default=True)),
                ('company_industry', models.CharField(max_length=50, default='')),
                ('company_sector', models.CharField(max_length=50, default='')),
                ('time_created', models.DateTimeField(default=datetime.datetime(2017, 5, 3, 0, 54, 42, 442216, tzinfo=utc))),
                ('encrypted', models.BooleanField(default=True)),
                ('ceo_name', models.CharField(max_length=20, default='')),
                ('date_created', models.DateField(default=datetime.datetime(2017, 5, 3, 0, 54, 42, 442276, tzinfo=utc))),
                ('company_email', models.CharField(max_length=50, default='')),
                ('key_piece', models.TextField(default='')),
                ('files', models.ManyToManyField(to='api.Attachment')),
                ('memgroups', models.ManyToManyField(blank=True, to='auth.Group')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Tags', help_text='A comma-separated list of tags.')),
            ],
        ),
    ]
