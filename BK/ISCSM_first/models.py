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
 	SW = ((Cisco,'Cisco'),(DrayTek,'DrayTek'),) 
 	SwitchType = models.CharField(max_length=5, choices=SW, default=DrayTek,)
	SwitchPort = models.CharField(max_length=10, blank=True,null=True)
	SwitchLocation = models.CharField(max_length=10,blank=True, null=True)
	Server = models.ForeignKey(ServerInfo)
	

	def __unicode__(self):
		return self.SwitchIP
	def __str__(self):
		return self.SwitchIP

class Firewall(models.Model):
	Server = models.ForeignKey(ServerInfo)		#nam tren BooLean
	Allow = models.BooleanField(default=True) #nam tren, duoi Foreign
	In = 'in'
 	Out = 'out'
 	Both = '2 way'
 	Wy = ((In,'IN'),(Out,'OUT'),(Both,'2 WAY'),)
 	Way = models.CharField(max_length=5, choices=Wy, default=In,)
  	Port = models.CharField(max_length=50,blank=True,null=True)
  	SourceIP = models.CharField(max_length=1000,blank=True,null=True)
  	DestinationIP = models.CharField(max_length=1000,blank=True,null=True)
  	Description = models.TextField(max_length=300,blank=True,null=True)
  	DateCreate =  models.DateField(default=datetime.today, blank=True, null=True)
  	#SourceIPsssss = models.CharField(max_length=1000,blank=True,null=True)

  	def __unicode__(self):
		return self.Description
	def __str__(self):
		return self.Port

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
	Owner = models.CharField(max_length=50,blank=True,null=True)

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
    pic = models.FileField()
    upload_date = models.DateTimeField(auto_now_add =True)

    def __unicode__(self):
    	return self.pic

	
class LogDelFile(models.Model):
    files = models.FileField()
    delete_date = models.DateTimeField(auto_now_add =True)
    user = models.TextField(max_length=50,blank=True,null=True)


