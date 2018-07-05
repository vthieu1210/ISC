# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.timezone import datetime
from datetime import date
import os
#from xlrd import *
# Create your views here.\
from models import Zone,ServerInfo,Service,Location,Firewall,Switch,Upload,LogDelFile
from network import verify_host,traceroute_host,telnet_host,status_service,winservice_owner,check_web,eventviewer,get_info_server,IIS_info
from importCSV import ReadFileCSV,SaveZone,SaveServerInfo,SaveLocation,SaveSwitch,SaveService,SaveFirewall,SaveDoc
from django.core.files.storage import FileSystemStorage



def index(request):
  return HttpResponseRedirect('/login')


@login_required
def default(request):
	lstZone=Zone.objects.all()
	testajax=ServerInfo.objects.get(IP='172.30.27.190')
	return render(request,'index.html',{'lstZone':lstZone, 'testajax':testajax})


@login_required(login_url='login/')
def showallserver(request):
	lstZone=Zone.objects.all()
	if request.method == 'POST':
		objZone=Zone.objects.get(id=int(request.POST.get('btn')))
		lstServer=_getServerZoneInfo(int(request.POST.get('btn')))
		return render(request,'datatables.html',{'lstServer':lstServer, 'objZone':objZone, 'lstZone':lstZone})
	return render(request,'datatables.html',{'lstZone':lstZone})


@login_required
def report(request):
	#result=IIS_info("172.20.18.26")
	lstreport=[]
	lstZone=Zone.objects.all()
	lstServer=ServerInfo.objects.all()
	SumServer=lstServer.count()
	for objZone in lstZone:
		SumZoneServer=ServerInfo.objects.filter(ZoneName_id=int(objZone.id)).count()
		Percent=round((float(SumZoneServer)/float(SumServer))*100, 2)
		lsttmp={'ZoneName':objZone.ZoneName,'ZoneName_id':objZone.id,'SumZoneServer':SumZoneServer,'Percent' : Percent}
		lstreport.append(lsttmp)
	return render(request,'report.html',{'SumServer':SumServer, 'lstreport':lstreport})
#		,'result':result})


@login_required
def reportfirewall(request):
	lstZone=Zone.objects.all()
	if request.method == 'POST' and request.POST.get('btn') == 'DateFW':
		m='%'+request.POST.get('datefwl')+'%'
#		datefw=Firewall.objects.raw('select * from ISCSM_firewall where DateCreate like %s' , [m])
		datefw=ServerInfo.objects.raw('select * from ISCSM_serverinfo join ISCSM_firewall on ISCSM_serverinfo.id = ISCSM_firewall.Server_id where DateCreate like %s' , [m])
		return render(request,'reportfw.html',{'datefw':datefw})
	else :
		datefw= ''
		return render(request,'reportfw.html',{'datefw':datefw, 'lstZone':lstZone})
#	y=2017	
#   m=04
#	firewall=Firewall.objects.all()
#	datefrom=date(y,m,01)
#	dateto=date(y,m+1,01)
#	datefw = []
#	for fire in firewall:
#		if fire.DateCreate is not None:
#			c = datetime.datetime.combine(fire.DateCreate, datetime.time(0,0))
#			c = fire.DateCreate
#			if c >= datefrom and c <= dateto:
#				datefw.append(fire)
#	return render(request,'tes.html',{'datefw':datefw})


@login_required
def showserver(request, pk):
	lstServer=_getServerInfo(pk)
	lstUpdate=''
	lstZone=Zone.objects.all()
	if request.method =='POST':
		lstUpdate=get_info_server(lstServer['IP'])
		lstServer['ServerType']=lstUpdate['ServerType']
		lstServer['ServerName']=lstUpdate['ServerName']
		lstServer['OS_Name']=lstUpdate['OS_Name']
		lstServer['CPU']=lstUpdate['CPU']
		lstServer['RAM']=lstUpdate['RAM']
		lstServer['HDD']=lstUpdate['HDD']
		objServerInfo=ServerInfo.objects.get(id=lstServer['id'])
		objServerInfo.ServerType=lstUpdate['ServerType']
		objServerInfo.ServerName=lstUpdate['ServerName']
		objServerInfo.OS_Name=lstUpdate['OS_Name']
		objServerInfo.CPU=lstUpdate['CPU']
		objServerInfo.RAM=lstUpdate['RAM']
		objServerInfo.HDD=lstUpdate['HDD']
		objServerInfo.save()
		return render(request,'abc.html',{'lstServer':lstServer, 'lstZone':lstZone})  
	return render(request,'abc.html',{'lstServer':lstServer, 'lstZone':lstZone})


@login_required
def showwinservices(request, pk):
	server=ServerInfo.objects.get(id=int(pk))
	result=status_service(server.IP)
	resultown=winservice_owner(server.IP)
	return render(request,'showwinsv.html',{'result':result, 'resultown':resultown})


@login_required
def showwebservices(request, pk):
	server=ServerInfo.objects.get(id=int(pk))
	if server.ZoneName.ZoneName == 'API' or server.ZoneName.ZoneName == 'Web Private' or server.ZoneName.ZoneName == 'Web Public':
		result=IIS_info(server.IP)
		return render(request,'showwebsv.html',{'result':result})
	else :
		error= 'Data not found'
		return render(request,'showwebsv.html',{'error':error})
 

@login_required
def importtb(request):
	lstZone=Zone.objects.all()
#	return render(request,'import.html',{'lstZone':lstZone})
	lst=''
	result=''
	try:
		if request.method == 'POST' and request.POST.get('btn') == 'Zone' :
			filecsv = request.FILES['csv_file']
			lst = ReadFileCSV(filecsv)
			result=SaveZone(lst)
			resok = '['+result.get('y0')+'] ->OK'
			resero= '['+result.get('y1')+'] ->EXISTS'
			return render(request, 'import.html', {'lst':resero, 'result':resok, 'lstZone':lstZone})
		if request.method == 'POST' and request.POST.get('btn') == 'Switch' :
			filecsv = request.FILES['csv_file']
			lst = ReadFileCSV(filecsv)
			result=SaveSwitch(lst)
			resok = '['+result.get('y0')+'] ->OK'
			resero= '['+result.get('y1')+'] ->EXISTS'
			return render(request, 'import.html', {'lst':resero, 'result':resok, 'lstZone':lstZone})
		if request.method == 'POST' and request.POST.get('btn') == 'Service' :
			filecsv = request.FILES['csv_file']
			lst = ReadFileCSV(filecsv)
			result = SaveService(lst)
			resok = '['+result.get('y0')+'] ->OK'
			resero= '['+result.get('y1')+'] ->EXISTS'
			return render(request, 'import.html', {'lst':resero, 'result':resok, 'lstZone':lstZone})
		if request.method == 'POST' and request.POST.get('btn') == 'Firewall' :
			filecsv = request.FILES['csv_file']
			lst = ReadFileCSV(filecsv)
			result=SaveFirewall(lst)
			resok = '['+result.get('y0')+'] ->OK'
			resero= '['+result.get('y1')+'] ->EXISTS'
			return render(request, 'import.html', {'lst':resero, 'result':resok, 'lstZone':lstZone})
		if request.method == 'POST' and request.POST.get('btn') == 'Location' :
			filecsv = request.FILES['csv_file']
			lst = ReadFileCSV(filecsv)
			result=SaveLocation(lst)
			resok = '['+result.get('y0')+'] ->OK'
			resero= '['+result.get('y1')+'] ->EXISTS'
			return render(request, 'import.html', {'lst':resero, 'result':resok, 'lstZone':lstZone})
		if request.method == 'POST' and request.POST.get('btn') == 'ServerInfo' :
			filecsv = request.FILES['csv_file']
			lst = ReadFileCSV(filecsv)
			result=SaveServerInfo(lst)
			resok = '['+result.get('y0')+'] ->OK'
			resero= '['+result.get('y1')+'] ->EXISTS'
			return render(request, 'import.html', {'lst':resero, 'result':resok, 'lstZone':lstZone})
	except:
		result='Please Choose File To Import'
		return render(request, 'import.html', {'lst':lst, 'result':result, 'lstZone':lstZone})
   
	return render(request,'import.html',{'lstZone':lstZone})


@login_required
def showeventview(request, pk):
	server=ServerInfo.objects.get(id=int(pk))
	result=eventviewer(server.IP, "app")
	resultsys=eventviewer(server.IP, "sys")
	return render(request,'eventviewer_temp.html',{'result':result, 'resultsys':resultsys})	


@login_required
def testservice(request, pk):
	service=Service.objects.get(id=int(pk))
	result=check_web(service.URLWEBS,service.Body,service.Header)
	return render(request,'testservice.html',{'result':result})



@login_required
def network(request): 

    if request.method == 'POST' and request.POST.get('btn') == 'Ping':
    	lstZone=Zone.objects.all()
        ip=request.POST.get('ipping')
        result=verify_host(ip)
 		
        return render(request, 'network.html',{'result':result, 'lstZone':lstZone})

    if request.method == 'POST' and request.POST.get('btn') == 'Tracert':
    	lstZone=Zone.objects.all()
        ip=request.POST.get('iptrace')
        result=traceroute_host(ip)
        return render(request, 'network.html',{'result':result, 'lstZone':lstZone})

    if request.method == 'POST' and request.POST.get('btn') == 'Telnet':
    	lstZone=Zone.objects.all()
        ip=request.POST.get('iptelnet')
        port=request.POST.get('porttelnet')
        result=telnet_host(ip,int(port))    
        return render(request, 'network.html',{'result':result, 'lstZone':lstZone})

    lstZone=Zone.objects.all()
    return render(request, 'network.html',{'lstZone':lstZone})



def _getServerZoneInfo(pk):
	lst=[]
	for serverid in __getServerZone(pk):
		lst.append(_getServerInfo(serverid))
	return lst



def _getServerInfo(pk):
	lst=''
	server=ServerInfo.objects.get(id=pk)
	LocationName=''
	Rack=''
	Unit=''

	for loc in Location.objects.all():
		if loc.Server_id==int(pk):
			LocationName=loc.LocationName
			Rack=loc.Rack
			Unit=loc.Unit
			break

	lst={
		#Sever Info
		'id'			:	server.id,
		'ServerName'	:	server.ServerName,
		'OS'			:	server.get_OS_display,
		'OS_Name'		:	server.OS_Name,
		'IP'			:	server.IP,
		'Function'		:	server.Function,
		'Description'	:	server.Description,
		'Link_Monitor'	:	server.Link_Monitor,
		#Zone
		'Zoneid'		:	server.ZoneName.id,
		'ZoneName'		:	server.ZoneName.ZoneName,
		'NetworkZone'	:	server.ZoneName.Network,
		'DescriptionZone':	server.ZoneName.Description,
		#Hardware
		'CPU'			:	server.CPU,
		'RAM'			:	server.RAM,
		'HDD'			:	server.HDD,
		'ServerType'	:	server.ServerType,
		#Location
		'LocationName'	:	LocationName,
		'Rack'			:	Rack,
		'Unit'			:	Unit,
		'Service'		:	{},
		'Firewall'		:	{},
		'Switch'		:	{},
	}
	for srvc in Service.objects.all():
		if srvc.Server_id == int(pk):
			lst['Service'][srvc.id]={
					'id'			:	srvc.id,
					'ServiceName'	:	srvc.ServiceName,
					'ServiceType'	:	srvc.get_ServiceType_display,
					'URL'			:	srvc.URL,
					'RunningAs'		:	srvc.RunningAs,
					'Description'	:	srvc.Description,
					'DateCreate'	:	srvc.DateCreate,
					'Owner'			:	srvc.Owner,
				}
	for fire in Firewall.objects.all():
		if fire.Server_id == int(pk):
			lst['Firewall'][fire.id]={
					'id'			:	fire.id,
					'Allow'			:	fire.Allow,
					'Way'			:	fire.get_Way_display,
					'Port'			:	fire.Port,
					'SourceIP'		:	fire.SourceIP,
					'DestinationIP'	:	fire.DestinationIP,
					'Description'	:	fire.Description,
					'DateCreate'	:	fire.DateCreate,
			}
	for swt in Switch.objects.all():
		if swt.Server_id == int(pk):
			lst['Switch'][swt.id]={
					'id'			:	swt.id,
					'SwitchIP'		:	swt.SwitchIP,
					'SwitchType'	:	swt.get_SwitchType_display,
					'SwitchPort'	:	swt.SwitchPort,
					'SwitchLocation':	swt.SwitchLocation,
			}

	return lst


def __getServerZone(pk):
	lst=[]
	zone=Zone.objects.get(id=pk)
	for srv in ServerInfo.objects.all():
		if srv.ZoneName.id==pk:
			lst.append(srv.id)
	return lst

@login_required
def home(request):
    if request.method == 'POST':
# 	upload file    	
    	if request.POST.get('updel') == 'upf' and request.FILES['myfile']:
    		myfile = request.FILES['myfile']
    		if request.POST.get('doctype') == 'DocA':
    			fs = FileSystemStorage(location='/home/django/ISC/media/tailieu/', base_url='/tailieu/')
    			errors = fs.url(myfile.name) +' : '+ handle_uploaded_file(fs.url(myfile.name),fs,myfile)
    			return render(request, 'simple_upload.html', {'errors':errors})
    		if request.POST.get('doctype') == 'DocB':
    			fs = FileSystemStorage(location='/home/django/ISC/media/quytrinh/', base_url='/quytrinh/')
    			errors = fs.url(myfile.name) +' : '+ handle_uploaded_file(fs.url(myfile.name),fs,myfile)
    			return render(request, 'simple_upload.html', {'errors':errors})
#	delete file tick
    	if request.POST.get('updel') == 'delf':
			passdel = request.POST.get('passw')
			if passdel in ["115","123"]:
				if request.POST.get('tick') != None:
					tick = request.POST.get('tick')
					errors = check_file_delete(tick,passdel)
					return render(request, 'simple_upload.html', {'errors':errors})
				if request.POST.get('tick') == None:
					errors = 'Choice file to delete'
					return render(request, 'simple_upload.html', {'errors':errors})
			else:
				errors = 'Nhap lai Password'
				return render(request, 'simple_upload.html', {'errors':errors})

#	delete file truc tiep			    	
#    	if request.POST.get('updel') == 'delf' and request.POST.get('doctype') != None and request.POST.get('tick') == None and request.FILES['myfile']:
#    		myfile = request.FILES['myfile']
#    		if request.POST.get('doctype') == 'DocA':
#	    		fs = FileSystemStorage(location='/home/django/ISC/media/tailieu/', base_url='/tailieu/')
#	    		errors = handle_uploaded_file(fs.url(myfile.name))
#	    		return render(request, 'simple_upload.html', {'errors':errors})
#	    	if request.POST.get('doctype') == 'DocB':
#	    		fs = FileSystemStorage(location='/home/django/ISC/media/quytrinh/', base_url='/quytrinh/')
#	    		errors = handle_uploaded_file(fs.url(myfile.name))
#	    		return render(request, 'simple_upload.html', {'errors':errors})
    	 
    else:
    	listfile = Upload.objects.all()
    	return render(request, 'simple_upload.html', {'listfile':listfile})


def check_file_delete(url,passdel):
	if os.path.exists('/home/django/ISC/media/'+url):
		try:
			os.remove('/home/django/ISC/media/'+url)
			Upload.objects.filter(pic=url).delete()
			if passdel == "115":
				usr = "Obama"
			elif passdel == "123":
				usr = "David"
			LogDelFile.objects.create(files=url, user=usr)
			errors = 'delete file thanh cong'
			return errors
#			Upload.objects.raw('delete from ISCSM_upload where pic = %s' , [asa])
		except OSError:
			pass
	else:
		errors = 'file khong ton tai'
		return errors

#    if not os.path.exists('home/'):
#        os.mkdir('home/')
 
#    with open('home/' + filename, 'wb+') as destination:
#        for chunk in file.chunks():
#            destination.write(chunk)

def handle_uploaded_file(url,fs,myfile):
	if os.path.exists('/home/django/ISC/media/'+url):
		errors = 'file da ton tai'
		return errors
	else:
		filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        dateup = datetime.now()
        Upload.objects.create(pic=uploaded_file_url)
        #SaveDoc(uploaded_file_url,dateup)
        errors = 'upload thanh cong'
        return errors
        
