from django.contrib import admin
from .models import Report
from .models import FullUserProfile
from .models import Message
from .models import Attachment
#from django.contrib.auth.models import Group

class PrivateInfo(admin.ModelAdmin):
    exclude = ('RSA_privatekey',)
admin.site.register(Report)
# Register your models here.
admin.site.register(FullUserProfile, PrivateInfo)
admin.site.register(Message)
admin.site.register(Attachment)
#admin.site.register(Group)
