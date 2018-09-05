# -*- coding: utf-8 -*-
from django.utils.timezone import datetime
from django.db import models
from django.forms import ModelForm
# Create your models here.
class Zone(models.Model):
    ZoneName = models.CharField(max_length=60)
    Description = models.TextField(max_length=300,blank=True,null=True)
    Network = models.GenericIPAddressField(protocol='IPv4',default=None, unique=True,blank=True,null=True)
    def __unicode__(self):
        return self.ZoneName
    def __str__(self):
        return self.ZoneName


class ServerInfo(models.Model):
    ServerName = models.CharField(max_length=50,blank=True,null=True)
    ZoneName = models.ForeignKey(Zone)
    IP = models.GenericIPAddressField(protocol='IPv4',unique=True)
    WD='wds'
    LN='lns'
    EX='exi'
    HDH = ((WD,'Windows'),(LN,'Linux'),(EX,'ESxi'),)
    OS = models.CharField(max_length=3, choices=HDH, default=LN,)
    OS_Name = models.CharField(max_length=200,blank=True,null=True)
    Function = models.CharField(max_length=200,blank=True,null=True)
    ServerType = models.CharField(max_length=200,blank=True,null=True)
    CPU = models.CharField(max_length=500,blank=True,null=True)
    RAM = models.CharField(max_length=200,blank=True,null=True)
    HDD = models.CharField(max_length=500,blank=True,null=True)
    Link_Monitor =  models.URLField(max_length=200, blank=True, null=True)
    Description = models.TextField(max_length=500,blank=True,null=True)


    def __unicode__(self):
        return self.ServerName
    def __str__(self):
        return self.ServerName


class Switch(models.Model):
    SwitchIP = models.GenericIPAddressField(protocol='IPv4', blank=True,null=True)
    Cisco='cso'
    DrayTek='dtk'
    Juniper='juniper'
    HPE='hpe'
    SW = ((Cisco,'Cisco'),(DrayTek,'DrayTek'),(Juniper,'Juniper'),(HPE,'HPE'))
    SwitchType = models.CharField(max_length=10, choices=SW, default=DrayTek,)
    SwitchPort = models.CharField(max_length=10, blank=True,null=True)
    SwitchLocation = models.CharField(max_length=10,blank=True, null=True)
    Server = models.ForeignKey(ServerInfo)


    def __unicode__(self):
        return self.SwitchIP
    def __str__(self):
        return self.SwitchIP

class Service(models.Model):
    ServiceName = models.CharField(max_length=50,blank=True,null=True)
    Win = 'win'
    Web = 'web'
    DB  = 'db'
    ST = ((Win,'win'),(Web,'web'),(DB,'db'),)
    ServiceType = models.CharField(max_length=5, choices=ST, default=Win,)
    URL =  models.URLField(max_length=200, blank=True, null=True)
    RunningAs = models.CharField(max_length=50,blank=True,null=True)
    Description = models.TextField(max_length=900, blank=True, null=True)
    Server = models.ForeignKey(ServerInfo)
    URLWEBS =  models.URLField(max_length=200, blank=True, null=True)
    Header = models.TextField(max_length=800,blank=True,null=True)
    Body = models.TextField(max_length=1000,blank=True,null=True)
    DateCreate =  models.DateField(default=datetime.today, blank=True, null=True)
    Author = models.CharField(max_length=50,blank=True,null=True)

    def __unicode__(self):
        return self.Description
    def __str__(self):
        return self.ServiceName


class Location(models.Model):
    LocationName = models.CharField(max_length=50,blank=True,null=True)
    Rack = models.CharField(max_length=50,blank=True,null=True)
    Unit = models.CharField(max_length=50,blank=True,null=True)
    Server = models.ForeignKey(ServerInfo)

    def __unicode__(self):
        return self.LocationName
    def __str__(self):
        return self.LocationName


class Upload(models.Model):
    file = models.FileField()
    filename = models.CharField(max_length=50, default='')
    category = models.CharField(max_length=50, default='')
    upload_date = models.DateTimeField(auto_now_add=True)
    creator = models.CharField(max_length=50, blank=True)
    del_flag = models.BooleanField(default=True)

    def __unicode__(self):
        return self.filename
    def __str__(self):
        return self.filename

class UploadCategory(models.Model):
    name = models.CharField(max_length=50, default='')
    path = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=50, default='')

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class WebService(models.Model):
    service_id = models.CharField(max_length=50, default='', unique=True)
    service = models.CharField(max_length=50, default='', unique=True)
    server = models.CharField(max_length=4000, default='')
    description = models.CharField(max_length=200, default='')
    ha = models.CharField(max_length=200, default='')
    path = models.CharField(max_length=4000, default='')
    author = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=4000, default='')
    protocol = models.CharField(max_length=4000, default='')
    ip_restrict = models.CharField(max_length=100, default='')
    del_flag = models.BooleanField(default=True)

    def __unicode__(self):
        return self.service
    def __str__(self):
        return self.service

class WinService(models.Model):
    service = models.CharField(max_length=50, default='', unique=True)
    server = models.CharField(max_length=4000, default='')
    description = models.CharField(max_length=200, default='')
    author = models.CharField(max_length=4000, default='')
    state = models.CharField(max_length=4000, default='')
    del_flag = models.BooleanField(default=True)

    def __unicode__(self):
        return self.service
    def __str__(self):
        return self.service

class FirewallRule(models.Model):
    src_ip = models.CharField(max_length=50, default='')
    dest_ip = models.CharField(max_length=4000, default='')
    port = models.CharField(max_length=4000, default='')
    description = models.CharField(max_length=4000, default='')
    datecreate =  models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.src_ip
    def __str__(self):
        return self.src_ip

class Task(models.Model):
    subject = models.CharField(max_length=4000, default='')
    start_date = models.CharField(max_length=50, default='')
    due_date = models.CharField(max_length=50, default='')
    done = models.CharField(max_length=50, default='')
    status = models.CharField(max_length=50, default='')
    assignee = models.CharField(max_length=50, default='')
    department = models.CharField(max_length=50, default='')
    tracker = models.CharField(max_length=50, default='')
    complexity = models.CharField(max_length=50, default='')
    estimated_time = models.CharField(max_length=50, default='')
    spent_time = models.CharField(max_length=50, default='')
    actual_end_date = models.CharField(max_length=50, default='')
    project = models.CharField(max_length=50, default='')

    def __unicode__(self):
        return self.subject
    def __str__(self):
        return self.subject
