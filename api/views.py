from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from .forms import ReportForm, LoginForm
from .models import Report, Attachment
from django.contrib.auth.models import User
from django.views.generic.edit import FormView, CreateView
from .forms import *
from django.contrib.auth.models import Group
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django.forms import model_to_dict
from django.template.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import *
from Crypto import Random
from Crypto.PublicKey import RSA
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import random
import string
import ast
from django.contrib.auth.models import User

#------------------Home Page functionality-------------------#

first = True
def index(request):
    try:
        user = User.objects.create_superuser(username='Site_Manager', password='admin', email='admin@admin.com')

        superuser = FullUserProfile()  # make fulluserprofile
        superuser.user = user
        superuser.user_type = "0"
        superuser.RSA_privatekey = "0"
        superuser.RSA_publickey = "0"
        superuser.save()
    except:
        pass

    # getting our template
    template = loader.get_template('html5up-arcana/index.html')
    # rendering the template in HttpResponse
    return HttpResponse(template.render())

def missionStatement(request):
    template = loader.get_template('html5up-arcana/mission-statement.html')
    return HttpResponse(template.render())

def about(request):
    template = loader.get_template('html5up-arcana/about.html')
    return HttpResponse(template.render())

def contactUs(request):
    template = loader.get_template('html5up-arcana/contact-us.html')
    return HttpResponse(template.render())

#------------------Register/Signup functionality-------------------#

def signup(request):
    form = SignupForm()

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/')

    token = {}
    token.update(csrf(request))
    token['form'] = form
    return render_to_response('signup.html', token)

#------------------Login functionality-------------------#

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                u=FullUserProfile.objects.get(user=user)
                usertype=u.user_type#this should return the usertype of the current user
                #return HttpResponseRedirect('/rango/')
                i = Message.objects.all().filter(message_to=username).__len__()
                return render(request, 'welcome.html', {'user_type': usertype, 'user': user, 'i':i})
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Lokahi account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            #print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        form=LoginForm()
        return render(request, 'login.html', {'form':form})

@login_required
def welcome(request):
    u = FullUserProfile.objects.get(user=request.user)
    user_type = u.user_type
    i = Message.objects.all().filter(message_to=request.user.username).__len__()
    template = loader.get_template('welcome.html')
    context = {'user_type': user_type, 'i':i}
    return HttpResponse(template.render(context, request))

@login_required
def success(request):
    template = loader.get_template("api/success.html")
    return render(request, 'success.html')

@login_required
def profile(request):
    u = FullUserProfile.objects.get(user=request.user)
    pub_key = u.RSA_publickey
    groupResults = request.user.groups.all()
    template = loader.get_template('profile.html')
    context = {'groupResults': groupResults, 'pub_key': pub_key}
    return HttpResponse(template.render(context, request))

#------------------Message functionality-------------------#

@login_required
def inbox(request):
    if request.method == "POST":
        messageResults = Message.objects.all().filter(message_to=request.user.username).order_by('time_created').reverse()
        #userList = User.objects.all()
        for i in messageResults:
            if(str(i.message_id) in request.POST):
                i.delete()

        messageResults = Message.objects.all().filter(message_to=request.user.username).order_by('time_created').reverse()
        template = loader.get_template('inbox.html')
        context = {'messageResults': messageResults, }
        return HttpResponse(template.render(context, request))
    else:
        #form = MessageForm()
        messageResults = Message.objects.all().filter(message_to=request.user.username).order_by('time_created').reverse()
        template = loader.get_template('inbox.html')
        context = {'messageResults': messageResults, }
        return HttpResponse(template.render(context, request))

@login_required
def secret_inbox(request):
    if request.method == "POST":
        messageResults = Message.objects.all().filter(message_to=request.user.username).order_by('time_created').reverse()
        for i in messageResults:
            if(str(i.message_id) in request.POST):
                #print("placeholder")
                targetUser = request.user
                targetMessageBody = str(i.message_body)
                targetMessageSubject = str(i.message_subject)
                u = FullUserProfile.objects.get(user=targetUser)
                prikey = u.RSA_privatekey
                prikey = RSA.importKey(prikey)

                i.message_body = dec_secret_string(targetMessageBody ,prikey)
                i.message_subject = dec_secret_string(targetMessageSubject, prikey)
                print(i.message_body)


        template = loader.get_template('secret_inbox.html')
        context = {'messageResults': messageResults, }
        return HttpResponse(template.render(context, request))
    else:
        #form = MessageForm()
        messageResults = Message.objects.all().filter(message_to=request.user.username).order_by('time_created').reverse()
        template = loader.get_template('secret_inbox.html')
        context = {'messageResults': messageResults, }
        return HttpResponse(template.render(context, request))


@login_required
def sent(request):
    if request.method == "POST":
        messageResults = Message.objects.all().filter(message_from=request.user.username).order_by('time_created').reverse()
        #userList = User.objects.all()
        for i in messageResults:
            if(str(i.message_id) in request.POST):
                i.delete()

        messageResults = Message.objects.all().filter(message_from=request.user.username).order_by('time_created').reverse()
        template = loader.get_template('sent.html')
        context = {'messageResults': messageResults, }
        return HttpResponse(template.render(context, request))
    else:
        #form = MessageForm()
        messageResults = Message.objects.all().filter(message_from=request.user.username).order_by('time_created').reverse()
        template = loader.get_template('sent.html')
        context = {'messageResults': messageResults, }
        return HttpResponse(template.render(context, request))

@login_required
def messageUser(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            messageResults = Message.objects.order_by('time_created').reverse()
            encchoice = form.cleaned_data['is_encrypted']
            if encchoice == 'Y':
                targetUser = User.objects.all().get(username=form.cleaned_data['message_to'])
                u = FullUserProfile.objects.get(user=targetUser)
                pubkey = u.RSA_publickey
                pubkey = RSA.importKey(pubkey)
                form.cleaned_data['message_subject'] = secret_string(form.cleaned_data['message_subject'], pubkey)
                form.cleaned_data['message_body'] = secret_string(form.cleaned_data['message_body'], pubkey)
                form.cleaned_data['message_from'] = str(request.user.username)
                form.save()
                template = loader.get_template('inbox.html')
                context = {'messageResults': messageResults, }
                return HttpResponse(template.render(context, request))
            else:
                form.cleaned_data['message_from'] = str(request.user.username)
                form.save()
                template = loader.get_template('inbox.html')
                context = {'messageResults': messageResults, }
                return HttpResponse(template.render(context, request))
        else:
            print("Form Not Valid")

    else:
        form = MessageForm()
        return render(request, 'messageUser.html', {'form': form})

def secret_string(string, public_key):
    string = string.strip()
    '''This returns a byte string encryption of the original string.
    Decrypting will return a byte string (considered valid from Piazza post)'''
    bstring = bytes(string, 'utf-8')
    enc_string = public_key.encrypt(bstring, 64)
    return enc_string

def dec_secret_string(string, private_key):
    dec_string = private_key.decrypt(ast.literal_eval(string))
    return dec_string

#------------------Site Manager functionality-------------------#

@login_required
def grantSMStatus(request):
    if request.method == "POST":
        userList = User.objects.order_by('username')
        #userList = User.objects.all()
        for i in userList:
            if(i.username in request.POST):
                i.is_superuser = True
                i.save()
                u = FullUserProfile.objects.get(user=i)
                u.user_type = "0"
                u.save()

        template = loader.get_template('grantSMStatus.html')
        context = {'userList': userList,}
        return HttpResponse(template.render(context, request))

    else:
        userList = User.objects.order_by('username')
        template = loader.get_template('grantSMStatus.html')
        context = {'userList': userList, }
        return HttpResponse(template.render(context, request))

@login_required
def addUsersToGroup(request):
    if request.method == "POST":
        userResults = User.objects.all()
        for i in userResults:
            if (str(i.username) in request.POST):
                return HttpResponseRedirect('assignUser/%s/' % i.username)
                #target = User.objects.all().filter(username = i.username)
                #template = loader.get_template('assignUser.html')
                #context = {'target': target, }
                #return HttpResponseRedirect(template.render(context, request))
                #return redirect('assignUser.html')
                #return render(request, 'success.html', context)
                # print("hello")
                # i.groups.add(request.POST)
                # i.save()
    else:
        userResults = User.objects.all()
        template = loader.get_template('addUsersToGroup.html')
        context = {'userResults': userResults, }
        return HttpResponse(template.render(context, request))

@login_required
def assignUser(request,target):
    if request.method == "POST":
        groupResults = Group.objects.all()
        for i in groupResults:
            if (str(i.name) in request.POST):
                targetGroup = Group.objects.get(name=i.name)
                targetUser = User.objects.all().get(username=str(target))
                targetUser.groups.add(targetGroup)
                targetUser.save()
                targetGroup.save()
                u = FullUserProfile.objects.get(user=request.user)
                user_type = u.user_type
                template = loader.get_template('welcome.html')
                context = {'targetGroup': targetGroup, 'user_type': user_type, }
                return HttpResponse(template.render(context, request))

    else:
        groupResults = Group.objects.all()
        template = loader.get_template('assignUser.html')
        context = {'groupResults': groupResults, }
        return HttpResponse(template.render(context, request))

"""def removeUserFromGroup(request):
    if request.method == "POST":
        userResults = User.objects.all()
        for i in userResults:
            groupResults = i.groups
            for x in groupResults:
                if (str(x.name) in request.POST):
                    print("placeholder")
                    template = loader.get_template('success.html')
                    context = {'userResults': userResults, }
                    return HttpResponse(template.render(context, request))

    else:
        userResults = User.objects.all()
        group_list = Group.objects.order_by('name')
        #groupResults = [[] for x in range(userResults.__len__())]
        #for i in userResults:
        #    for j in i.groups:
        #        groupResults[i][j] = i.groups
        template = loader.get_template('removeUserFromGroup.html')
        context = {'userResults': userResults, }
        return HttpResponse(template.render(context, request))"""

@login_required
def removeUserFromGroup(request):
    if request.method == "POST":
        userResults = User.objects.all()
        for i in userResults:
            # print(i.message_id)
            if (str(i.username) in request.POST):
                return HttpResponseRedirect('removeUser/%s/' % i.username)
                #target = User.objects.all().filter(username = i.username)
                #template = loader.get_template('assignUser.html')
                #context = {'target': target, }
                #return HttpResponseRedirect(template.render(context, request))
                #return redirect('assignUser.html')
                #return render(request, 'success.html', context)
                # print("hello")
                # i.groups.add(request.POST)
                # i.save()
    else:
        userResults = User.objects.all()
        template = loader.get_template('removeUserFromGroup.html')
        context = {'userResults': userResults, }
        return HttpResponse(template.render(context, request))

@login_required
def removeUser(request,target):
    if request.method == "POST":
        targetUser = User.objects.all().get(username=str(target))
        groupResults = targetUser.groups.all()
        for i in groupResults:
            #print(target)
            if (str(i.name) in request.POST):
                targetGroup = Group.objects.get(name=i.name)
                targetGroup.user_set.remove(targetUser)
                targetUser.save()
                targetGroup.save()
                u = FullUserProfile.objects.get(user=request.user)
                user_type = u.user_type
                template = loader.get_template('welcome.html')
                context = {'targetGroup': targetGroup, 'user_type': user_type, }
                return HttpResponse(template.render(context, request))

    else:
        targetUser = User.objects.all().get(username=str(target))
        groupResults = targetUser.groups.all()
        template = loader.get_template('removeUser.html')
        context = {'groupResults': groupResults, }
        return HttpResponse(template.render(context, request))

@login_required
def suspendRestore(request):
    if request.method == "POST":
        userList = User.objects.order_by('username')
        #userList = User.objects.all()
        for i in userList:
            if(i.username in request.POST):
                i.is_active = not (i.is_active)
                i.save()

        template = loader.get_template('suspend-restore-user-access.html')
        context = {'userList': userList,}
        return HttpResponse(template.render(context, request))

    else:
        userList = User.objects.order_by('username')
        template = loader.get_template('suspend-restore-user-access.html')
        context = {'userList': userList, }
        return HttpResponse(template.render(context, request))

@login_required
def viewReportsSM(request):
    print("placeholder")
    report_list = Report.objects.all()
    context = {'report_list': report_list}
    return render(request, 'viewReportsSM.html', context)

@login_required
def deleteReportSM(request, report_id):
    if Report.objects.filter(pk = report_id):
        deletedReport = Report.objects.get(pk = report_id)
        deletedReport.delete()

        report_list = Report.objects.all()
        context = {'report_list': report_list}
        return render(request, 'viewReportsSM.html', context)
    else:
        return HttpResponse("No report with that ID was found")

@login_required
def singleReportSM(request, report_id):
    if request.method == "GET":
        selected_report = Report.objects.get(pk=report_id);
        context = {'selected_report': selected_report};
        return render(request, 'reportSM.html', context)
    else:
        return HttpResponse("Invalid request method");



#------------------Group functionality-------------------#

@login_required
def createGroup(request):
    if request.method == "POST":
        form = createGroupForm(request.POST)
        if(form.is_valid()):
            #form.save()
            groupResults = Group.objects.order_by('name')
            template = loader.get_template('welcome.html')
            u = FullUserProfile.objects.get(user=request.user)
            user_type = u.user_type
            context = {'groupResults': groupResults, 'user_type': user_type}
            group_name = form.cleaned_data['group_name']
            newGroup = Group.objects.create(name=group_name)
            #print(newGroup)
            #make this public key only or hash. then encryption can happen with this for all members of a group.
            request.user.groups.add(newGroup)
            request.user.save()
            return HttpResponse(template.render(context, request))
    else:
        form = createGroupForm()
        return render(request, 'createGroup.html', {'form': form})

@login_required
def removeSelfFromGroup(request):
    print("placeholder")
    if request.method == "POST":
        #targetUser = User.objects.all().get(username=str(target))
        targetUser = request.user
        groupResults = targetUser.groups.all()
        for i in groupResults:
            if (str(i.name) in request.POST):
                targetGroup = Group.objects.get(name=i.name)
                targetGroup.user_set.remove(targetUser)
                targetUser.save()
                targetGroup.save()
                u = FullUserProfile.objects.get(user=request.user)
                user_type = u.user_type
                template = loader.get_template('welcome.html')
                context = {'targetGroup': targetGroup, 'user_type': user_type, }
                return HttpResponse(template.render(context, request))

    else:
        #targetUser = User.objects.all().get(username=str(target))
        targetUser = request.user
        groupResults = targetUser.groups.all()
        template = loader.get_template('removeSelfFromGroup.html')
        context = {'groupResults': groupResults, }
        return HttpResponse(template.render(context, request))

@login_required
def addUsersToMemberGroup(request):
     if request.method == "POST":
        userResults = User.objects.all()
        for i in userResults:
            if (str(i.username) in request.POST):
                return HttpResponseRedirect('assignUserToMemberGroup/%s/' % i.username)
     else:
        userResults = User.objects.all()
        template = loader.get_template('addUsersToMemberGroup.html')
        context = {'userResults': userResults, }
        return HttpResponse(template.render(context, request))

@login_required
def assignUserToMemberGroup(request, target):
    if request.method == "POST":
        #groupResults = Group.objects.all()
        groupResults = request.user.groups.all()
        for i in groupResults:
            if (str(i.name) in request.POST):
                targetGroup = Group.objects.get(name=i.name)
                targetUser = User.objects.all().get(username=str(target))
                targetUser.groups.add(targetGroup)
                targetUser.save()
                targetGroup.save()
                u = FullUserProfile.objects.get(user=request.user)
                user_type = u.user_type
                template = loader.get_template('welcome.html')
                context = {'targetGroup': targetGroup, 'user_type': user_type, }
                return HttpResponse(template.render(context, request))

    else:
        groupResults = request.user.groups.all()
        template = loader.get_template('assignUserToMemberGroup.html')
        context = {'groupResults': groupResults, }
        return HttpResponse(template.render(context, request))


#------------------Report functionality-------------------#

#@login_required
#@user_passes_test(lambda u: u.is_superuser or u.siteuser.usertype is not 'i')
@login_required
def reportUpload(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()
            u = FullUserProfile.objects.get(user=request.user)
            report.key_piece = u.RSA_publickey
            report.save()
            for each in form.cleaned_data['files']:
                attfile = Attachment.objects.create(file=each)
                report.files.add(attfile)
                #form.files[] = attfile


            return render(request, 'success.html')
    else:
        form = ReportForm()
    return render(request, 'reportUpload.html', {'form': form})

    #template_name = 'reportUpload.html'
    # form_class = ReportForm
    # success_url = '/success'
    #
    # def form_valid(self, form):
    #     for each in form.cleaned_data['attachments']:
    #         Attachment.objects.create(file=each)
    #     return super(UploadView, self).form_valid(form)
    # model = Report
    # form_class = ReportForm
    # template_name = 'reportUpload.html'
    # success_url = '/success'

@login_required
def reportView(request, report_id):
    if Report.objects.filter(id=report_id):
        repo = Report.objects.get(report_id)
    else:
        return HttpResponse("No report with that ID was found")
    if request.method == "GET":
        if Report.objects.filter(id=report_id):
            report_Dict = model_to_dict(repo)
        return render(request, 'report.html', report_Dict)

@login_required
def singleReport(request, report_id):
    if request.method == "GET":
        selected_report = Report.objects.get(pk=report_id);
        context = {'selected_report': selected_report};
        return render(request, 'report.html', context)

    else:
        return HttpResponse("Invalid request method");

@login_required
def singleReportInv(request, report_id):
    if request.method == "GET":
        selected_report = Report.objects.get(pk=report_id);
        context = {'selected_report': selected_report};
        return render(request, 'reportInvestor.html', context)
    
    else:
        return HttpResponse("Invalid request method");

@login_required
def viewReports(request):
    #report_list = Report.objects.filter(private=False)
    report_list = Report.objects.filter(Q(private=False) | Q(memgroups__in=request.user.groups.all()))

    #u = FullUserProfile.objects.get(user=request.user)
    #groupResults = request.user.groups.all()
    #user_type = u.user_type
    context = {'report_list': report_list}
    return render(request, 'viewReports.html', context)

@login_required
def viewReportsInv(request):
    #report_list = Report.objects.filter(private=False)
    report_list = Report.objects.filter(Q(private=False) | Q(memgroups__in=request.user.groups.all()))
    
    #u = FullUserProfile.objects.get(user=request.user)
    #groupResults = request.user.groups.all()
    #user_type = u.user_type
    context = {'report_list': report_list}
    return render(request, 'viewReportInvestor.html', context)

@login_required
def deleteReport(request, report_id):
    if Report.objects.filter(pk = report_id):
        deletedReport = Report.objects.get(pk = report_id)
        deletedReport.delete()

        report_list = Report.objects.all()
        context = {'report_list': report_list}
        return render(request, 'viewReports.html', context)
    else:
        return HttpResponse("No report with that ID was found")

# this edit report is for company users - they can edit all fields but not add files
@login_required
def editReport(request, report_id):
    selected_report = get_object_or_404(Report, pk = report_id)
    context = {'selected_report' : selected_report};
    
    form = ReportForm(request.POST, request.FILES)
    print(form.errors)
    if form.is_valid():
        selected_report.delete()
        report = form.save()
        for each in form.cleaned_data['files']:
            attfile = Attachment.objects.create(file=each)
            report.files.add(attfile)
        return render(request, 'success.html')
    else:
        form = ReportForm()
    return render(request, 'editReport.html', context)

# this edit report is for investor users - they can add files but not edit fields
@login_required
def editReportI(request, report_id):
    selected_report = get_object_or_404(Report, pk = report_id)
    context = {'selected_report' : selected_report};
    if request.method == 'POST' and request.FILES['files']:
        for each in request.FILES.getlist('files'):
            attfile = Attachment.objects.create(file=each)
            selected_report.files.add(attfile)
        return render(request, 'success.html')
    return render(request, 'editReportInvestor.html', context)

@login_required
def searchReports(request):
    if request.method == "POST":
        searched_Reports = Report.objects.all()

        get_compname = request.POST['searchCompanyName']
        if get_compname != "":
            searched_Reports = Report.objects.filter(company_name=get_compname)

        get_ceoname = request.POST['searchCEOName']
        if get_ceoname != "":
            searched_Reports = searched_Reports.filter(ceo_name=get_ceoname)

        get_location = request.POST['searchCompanyLoc']
        if get_location != "":
            searched_Reports = searched_Reports.filter(company_location=get_location)

        get_country = request.POST['searchCompanyCountry']
        if get_country != "":
            searched_Reports = searched_Reports.filter(company_country=get_country)

        get_project = request.POST['searchCompanyProjects']
        if get_project != "":
            searched_Reports = searched_Reports.filter(current_projects=get_project)

        get_time = request.POST['searchReportDate']
        if get_time != "":
            #print(get_time)
            #get_time = str(get_time)
            #print(type(get_time))
            searched_Reports = searched_Reports.filter(date_created=get_time)


        get_sector = request.POST['searchCompanySector']
        if get_sector != "" and get_sector != " ":
            searched_Reports = searched_Reports.filter(company_sector=get_sector)

        get_industry = request.POST['searchCompanyIndustry']
        if get_industry != "" and get_industry != " ":
            searched_Reports = searched_Reports.filter(company_industry=get_industry)

        searched_Reports = searched_Reports.filter(Q(private=False) | Q(memgroups__in=request.user.groups.all()))


        context = {'searched_Reports' : searched_Reports}
        return render(request, 'searchedReports.html', context)
    else:
        return render(request, 'searchReports.html')




