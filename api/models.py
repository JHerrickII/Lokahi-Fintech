from django.db import models
import os
import string
import random
from taggit.managers import TaggableManager
from django.utils.timezone import now as timezone_now
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import datetime

from django.utils.translation import ugettext_lazy as _

# Create your models here.
from Lokahi import settings


def create_random_string(length=10):
    if length<=0:
        length=10
    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])

class Attachment(models.Model):
    file=models.FileField(upload_to='tmp')
    #reports = models.ManyToManyField('Report')

    def filename(self):
        return os.path.basename(self.file.name)

def upload_to(instance, filename):
    now=timezone_now()
    filename_base, filename_ext=os.path.splitext(filename)
    return 'my_uploads/{}_{}{}'.format(now.strftime("%Y/%m/%d/%Y%m%d%H%M%S"), create_random_string(),filename_ext.lower())

class Report(models.Model):
    report_name = models.CharField(max_length = 200, default="")
    #report_file_name = models.CharField(max_length=200, default="")
    report_files = models.FileField(upload_to='documents', null=True, blank = True)
    company_name = models.CharField(max_length=50, default="")
    company_phone = models.CharField(max_length=11, default="")
    company_location = models.CharField(max_length=50, default="")
    company_country = models.CharField(max_length=20, default="")
    business_type = models.CharField(max_length=20, default="")
    #current_projects = models.CharField(max_length= 200, default="")
    current_projects = models.TextField(max_length=100, default="")
    private = models.BooleanField(default=True)
    company_industry = models.CharField(max_length=50, default="")
    company_sector = models.CharField(max_length=50, default="")
    files = models.ManyToManyField(Attachment)
    #groups m2m w Group
    memgroups = models.ManyToManyField(Group, blank=True)
    #time_created = models.DateTimeField(auto_now_add=True)
    time_created = models.DateTimeField(default=timezone_now())
    encrypted = models.BooleanField(default=True)
    #tags = TaggableManager()
    ceo_name = models.CharField(max_length=20, default="")
    date_created = models.DateField(default=timezone_now())
    #date_created = models.DateField(auto_now_add=True)
    company_email = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.report_name
    tags = TaggableManager()
    key_piece = models.TextField(default="")
class FullUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_type = models.CharField(max_length=200)


    RSA_publickey = models.TextField(default="")
    RSA_privatekey = models.TextField(default="")



class Message(models.Model):
    OPTIONS = (('Y', 'Yes'),
               ('N', 'No'),)

    message_encrypt = models.CharField(max_length=1, choices=OPTIONS)
    message_subject = models.CharField(max_length=2000)
    message_body = models.CharField(max_length=2000)
    message_from = models.CharField(max_length=200)
    message_to = models.CharField(max_length=200)
    message_delete = models.CharField(max_length=1, choices=OPTIONS)
    message_id = models.AutoField(primary_key=True)
    #time_created = models.DateTimeField(default=timezone_now())
    time_created = models.DateTimeField(auto_now_add=True, blank=True)

    def encrypt(self):
        print("placeholder")

    def decrypt(self):
        print("placeholder")


