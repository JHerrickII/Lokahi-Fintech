from django import forms
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Report, Attachment
#from .models import create_group
from .models import Message
from django import forms
from multiupload.fields import MultiFileField
#from .models import edit_group
from django.contrib.auth.forms import UserCreationForm
from .models import FullUserProfile
from django.contrib.auth.models import Group
from Crypto import Random
from Crypto.PublicKey import RSA
from fda.encryption import decr_hash, priv_hash

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_name','company_name', 'company_phone',
                  'company_location', 'company_country', 'business_type',
                  'current_projects', 'private',
                  'company_industry', 'company_sector', 'memgroups', 'encrypted', 'ceo_name', 'company_email']

    files = MultiFileField(min_num=1, max_num=20, max_file_size=1024*1024*5, required=False)
    memgroups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)

class UploadForm(forms.Form):
    files = MultiFileField(min_num=1, max_num=20, max_file_size=1024*1024*5, required=False)



class LoginForm(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50, widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    CHOICES = (('1', 'Investor',), ('2', 'Company',))
    user_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    username = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name','user_type', 'email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        random_g = Random.new().read
        RSAkey = RSA.generate(1024, random_g)
        r_pub=RSAkey.publickey().exportKey()
        r_pri=RSAkey.exportKey()
        user.RSA_privatekey = r_pri
        user.RSA_publickey = r_pub
        if commit:
            user.save()# take out of full user profile the privatekey
        FullUserProfile.objects.create(user=user, RSA_privatekey=r_pri, RSA_publickey = r_pub, user_type=self.cleaned_data['user_type'])

        return user

class MessageForm(forms.ModelForm):
    OPTIONS = (('Y', 'Yes'),
               ('N', 'No'),)
    is_encrypted = forms.ChoiceField(required=True, choices=OPTIONS, help_text="Encrypt this Message?")
    message_subject = forms.CharField(required=True, help_text="Subject")
    message_body = forms.CharField(required=True, help_text="Message Text", widget=forms.Textarea)
    message_to = forms.CharField(required=True, help_text="Message Recipient")
    #message_from = forms.CharField(required=True, help_text="Message Sender")


    class Meta:
        model = Message
        fields = ("is_encrypted", "message_subject", "message_body", "message_to")

    def save(self, commit=True):
        message_to = self.cleaned_data['message_to']
        message_from = self.cleaned_data['message_from']
        message_subject = self.cleaned_data['message_subject']
        message_body = self.cleaned_data['message_body']
        is_encrypted = self.cleaned_data['is_encrypted']
        #message_list = []

        msg = Message(
            message_to = message_to,
            message_from = message_from,
            message_subject = message_subject,
            message_body = message_body,
            message_encrypt = is_encrypted
        )

        msg.save()
        #message_list.append(msg)

        #return message_list
        return msg


class createGroupForm(forms.Form):
    group_name = forms.CharField(required=True, max_length=20)

    class Meta:
        model = Group
        fields = ('group_name',)

    #def save(self, commit=True):
       # group_name = self.cleaned_data['group_name']
        #newGroup = Group.objects.create(name=group_name)
        #newGroup.name = str(self.cleaned_data['name'])
        #request.user.groups.add(newGroup)
        #newGroup.save()
        #return newGroup

class addMembersToGroupForm(forms.Form):
    #print("placeholder")
    group_name = forms.CharField(required=True, help_text="Group Name", max_length=20)
    users_list = forms.MultipleChoiceField(required=True,widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Group
        fields = ('group_name')
