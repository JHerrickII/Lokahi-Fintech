from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
               url(r'^reportUpload/', views.reportUpload),
               url(r'^success', views.success),
               url(r'^viewReports/', views.viewReports),
               url(r'^viewReportsInvestor/', views.viewReportsInv),
               url(r'^viewReports/(?P<report_id>[\w|\W]+)/$', views.reportView),
               url(r'^singleReport/(?P<report_id>[0-9]+)/$', views.singleReport),
               url(r'^singleReportInvestor/(?P<report_id>[0-9]+)/$', views.singleReportInv),
               url(r'^editReport/(?P<report_id>[0-9]+)/$', views.editReport),
               url(r'^editReportI/(?P<report_id>[0-9]+)/$', views.editReportI),
               url(r'^deleteReport/(?P<report_id>[0-9]+)/$', views.deleteReport),
               url(r'^$', views.index),
               url(r'^mission-statement', views.missionStatement),
               url(r'^about', views.about),
               url(r'^contact-us', views.contactUs),
               url(r'^signup', views.signup, name = 'signup'),
               url(r'^login/$', views.user_login, name='login'),
               url(r'^logout/$', auth_views.logout, {'next_page' : '/'}, name = 'logout'),
               url(r'^welcome/', views.welcome, name='welcome'),
               url(r'^searchReports', views.searchReports),
               url(r'^searchedReports', views.searchReports),
               url(r'^createGroup', views.createGroup),
               url(r'^messageUser', views.messageUser),
               url(r'^inbox', views.inbox),
               url(r'^sent', views.sent),
               url(r'^suspendRestoreAccess', views.suspendRestore),
               url(r'^addUsersToGroup', views.addUsersToGroup),
               url(r'^grantSMStatus', views.grantSMStatus),
               url(r'^assignUser/(?P<target>\w+)/$', views.assignUser, name='assignUser'),
               url(r'removeUserFromGroup', views.removeUserFromGroup),
               url(r'^removeUser/(?P<target>\w+)/$', views.removeUser, name='removeUser'),
               url(r'^removeSelfFromGroup', views.removeSelfFromGroup),
               url(r'^addUsersToMemberGroup', views.addUsersToMemberGroup),
               url(r'^assignUserToMemberGroup/(?P<target>\w+)/$', views.assignUserToMemberGroup, name='assignUserToMemberGroup'),
               url(r'^profile', views.profile),
               url(r'^viewReportsSM', views.viewReportsSM),
               url(r'^deleteReportSM/(?P<report_id>[0-9]+)/$', views.deleteReportSM),
               url(r'^singleReportSM/(?P<report_id>[0-9]+)/$', views.singleReportSM),
               url(r'^secretInbox', views.secret_inbox),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

