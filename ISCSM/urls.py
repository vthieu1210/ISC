"""ISC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth.views import login
from django.conf import settings
from django.conf.urls import include, url

from .views import *

app_name="ISCSM"
urlpatterns = [
    url(r'^showall/$', showallserver),
    url(r'^showall/(?P<pk>\d+)/$', showserver),
 	url(r'^$', index, name='index'),
	url(r'^login', login, {'template_name': 'login.html'}),
	url(r'^logout', logOut, name='logout'),
    url(r'^accounts/login/$', login, {'template_name': 'login.html'}),
    url(r'testservice/(?P<pk>\d+)/$', testservice),
    url(r'showwinservices/(?P<pk>\d+)/$', showwinservices),
    url(r'showwebservices/(?P<pk>\d+)/$', showwebservices),
    url(r'showeventview/(?P<pk>\d+)/$', showeventview),
    url(r'^import/$', importtb),
    url(r'^report/$', report),
    url(r'^report/web_service$', reportWebService, name='report_web_service'),
    url(r'^report/win_service$', reportWinService, name='report_win_service'),
    url(r'^report/firewall_rule$', reportFirewallRule, name='report_firewall_rule'),
    url(r'^report/handle_firewall_rule$', handleFirewallRule, name='handle_firewall_rule'),
    url(r'^reportfw/$', reportfirewall),
    url(r'^network', network, name='network'),
    url(r'^document', document, name='document'),
    url(r'^handle_document$', handleDocument, name='handle_document'),
    url(r'^radius', radius, name='radius'),
    url(r'^monitor_radius', monitorRadius, name='monitor_radius'),
    url(r'^log_task', logTask, name='log_task'),
    url(r'^export_task', exportTask, name='export_task'),
]
