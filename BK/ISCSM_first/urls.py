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
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth.views import login

from .views import showallserver,default,index,showserver,showwinservices,showwebservices,importtb,showeventview,testservice,network,report,reportfirewall,home
#from .views import showallserver,showserver,index,network,testservice,showwinservices,showeventview,default,importtb
urlpatterns = [
    url(r'^showall/$', showallserver),
    url(r'^showall/(?P<pk>\d+)/$', showserver),
 	url(r'^$', index),
	url(r'^login/$', login, {'template_name': 'login.html'}),
    #url(r'^test/$', RedirectView.as_view(url='http://210.245.31.173:8080/telnet/radius',permanent=False), name='test',),
    url(r'testservice/(?P<pk>\d+)/$', testservice),
    url(r'showwinservices/(?P<pk>\d+)/$', showwinservices),
    url(r'showwebservices/(?P<pk>\d+)/$', showwebservices),
    url(r'showeventview/(?P<pk>\d+)/$', showeventview),
    url(r'^network/$', network),
    url(r'^default/$', default),
    url(r'^import/$', importtb),
    url(r'^report/$', report),
    url(r'^reportfw/$', reportfirewall),
    url(r'^home/$', home, name='imageupload'),
#    url(r'^list/$', list, name='list'),
]
