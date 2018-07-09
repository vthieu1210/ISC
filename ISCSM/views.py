# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import datetime
from django.core.files.storage import FileSystemStorage

import os, threading, sys, urllib, csv
import timeout_decorator

from xlrd import *
from pyexcel_xlsx import *
from datetime import date
from models import *
from importCSV import *
from validate import *
from forms import *
from utility.document import *
from utility.network import *
from utility.radius import *
from utility.firewall_rule import *
from utility.web_service import *
from utility.win_service import *

from ISC.settings import MEDIA_URL, MEDIA_ROOT

@login_required
def logOut(request):
    logout(request)
    return HttpResponseRedirect(reverse('ISCSM:index'))

@login_required
def index(request):
    lstZone=Zone.objects.all()
    testajax=ServerInfo.objects.get(IP='172.30.27.190')
    return render(request,'index.html',{'lstZone':lstZone, 'testajax':testajax,'result':'result'})

@login_required
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
    #,'result':result})

@login_required
def reportfirewall(request):
    lstZone=Zone.objects.all()
    if request.method == 'POST' and request.POST.get('btn') == 'DateFW':
        m='%'+request.POST.get('datefwl')+'%'
        #datefw=Firewall.objects.raw('select * from ISCSM_firewall where DateCreate like %s' , [m])
        datefw=ServerInfo.objects.raw('select * from ISCSM_serverinfo join ISCSM_firewall on ISCSM_serverinfo.id = ISCSM_firewall.Server_id where DateCreate like %s' , [m])
        return render(request,'reportfw.html',{'datefw':datefw})
    else :
        datefw= ''
        return render(request,'reportfw.html',{'datefw':datefw, 'lstZone':lstZone})
    #y=2017
    #m=04
    #firewall=Firewall.objects.all()
    #datefrom=date(y,m,01)
    #dateto=date(y,m+1,01)
    #datefw = []
    #for fire in firewall:
        #if fire.DateCreate is not None:
            #c = datetime.datetime.combine(fire.DateCreate, datetime.time(0,0))
            #c = fire.DateCreate
            #if c >= datefrom and c <= dateto:
                #datefw.append(fire)
    #return render(request,'tes.html',{'datefw':datefw})

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
    resultown=winservice_author(server.IP)
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
    #return render(request,'import.html',{'lstZone':lstZone})
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
        'id'            :    server.id,
        'ServerName'    :    server.ServerName,
        'OS'            :    server.get_OS_display,
        'OS_Name'        :    server.OS_Name,
        'IP'            :    server.IP,
        'Function'        :    server.Function,
        'Description'    :    server.Description,
        'Link_Monitor'    :    server.Link_Monitor,
        #Zone
        'Zoneid'        :    server.ZoneName.id,
        'ZoneName'        :    server.ZoneName.ZoneName,
        'NetworkZone'    :    server.ZoneName.Network,
        'DescriptionZone':    server.ZoneName.Description,
        #Hardware
        'CPU'            :    server.CPU,
        'RAM'            :    server.RAM,
        'HDD'            :    server.HDD,
        'ServerType'    :    server.ServerType,
        #Location
        'LocationName'    :    LocationName,
        'Rack'            :    Rack,
        'Unit'            :    Unit,
        'Service'        :    {},
        'Firewall'        :    {},
        'Switch'        :    {},
    }
    for srvc in Service.objects.all():
        if srvc.Server_id == int(pk):
            lst['Service'][srvc.id]={
                    'id'            :    srvc.id,
                    'ServiceName'    :    srvc.ServiceName,
                    'ServiceType'    :    srvc.get_ServiceType_display,
                    'URL'            :    srvc.URL,
                    'RunningAs'        :    srvc.RunningAs,
                    'Description'    :    srvc.Description,
                    'DateCreate'    :    srvc.DateCreate,
                    'author'            :    srvc.Author,
                }
    for swt in Switch.objects.all():
        if swt.Server_id == int(pk):
            lst['Switch'][swt.id]={
                    'id'            :    swt.id,
                    'SwitchIP'        :    swt.SwitchIP,
                    'SwitchType'    :    swt.get_SwitchType_display,
                    'SwitchPort'    :    swt.SwitchPort,
                    'SwitchLocation':    swt.SwitchLocation,
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
def reportWebService(request):
    #if request.GET.get('action') == 'retrieveData':
    if request.method == 'POST':
        id = request.POST.get('id')
        description = request.POST.get('description')
        ha = request.POST.get('ha')
        author = request.POST.get('author')
        ip_restrict = request.POST.get('ip_restrict')
        updateWebServiceDescript(id, description, ha, author, ip_restrict)

        return redirect(reverse('ISCSM:report_web_service'))

    search = {
        'service':      request.GET.get('service'),
        'server':       request.GET.get('server'),
        'path':         request.GET.get('path'),
        'state':        request.GET.get('state'),
        'protocol':     request.GET.get('protocol'),
        'author':       request.GET.get('author'),
    }

    services = WebService.objects.all()
    services = searchWebService(services, search['service'], search['server'], search['state'], search['path'], search['protocol'], search['author'])
    for service in services:
        service.server = service.server.split(';')
        service.path = service.path.split(';')
        service.state = service.state.split(';')
        service.protocol = service.protocol.split(';')

    if request.GET.get('row'):
        row = request.GET.get('row')
    else:
        row = 5
    paginator = Paginator(services, row)

    page = request.GET.get('page')

    try:
        listservice = paginator.page(page)
    except PageNotAnInteger:
        listservice = paginator.page(1)
    except EmptyPage:
        listservice = paginator.page(paginator.num_pages)

    return render(request, 'report_web_service.html', {'listservice' : listservice,
                                                       'total_services' : len(services),
                                                       'search' : search,
                                                       'row' : row,})

@login_required
def reportWinService(request):
        if request.method == 'POST':
            id = request.POST.get('id')
            description = request.POST.get('description')
            updateWinServiceDescript(id, description)

            return redirect(reverse('ISCSM:report_win_service'))

        search = {
            'service':      request.GET.get('service'),
            'server':       request.GET.get('server'),
            'author':       request.GET.get('author'),
            'state':        request.GET.get('state'),
            'type':        request.GET.get('type')
        }

        services = WinService.objects.all()
        services = searchWinService(services, search['service'], search['server'], search['state'], search['author'], search['type'])
        for service in services:
            service.server = service.server.split(';')
            service.author = service.author.split(';')
            service.state = service.state.split(';')

        if request.GET.get('row'):
            row = request.GET.get('row')
        else:
            row = 5
        paginator = Paginator(services, row)

        page = request.GET.get('page')

        try:
            listservice = paginator.page(page)
        except PageNotAnInteger:
            listservice = paginator.page(1)
        except EmptyPage:
            listservice = paginator.page(paginator.num_pages)

        return render(request, 'report_win_service.html', {'listservice' : listservice,
                                                           'total_services' : len(services),
                                                           'search' : search,
                                                           'row' : row,})

@login_required
def reportFirewallRule(request):
    rules = FirewallRule.objects.all()
    search = {}
    if request.GET.get('action') == 'search':
        search = {
            'src_ip':                   request.GET.get('src_ip'),
            'dest_ip':                  request.GET.get('dest_ip'),
            'port':                     request.GET.get('port'),
            'description':              request.GET.get('description'),
            'search_by_date_type':      request.GET.get('search_by_date_type'),
            'is_datecreate':            request.GET.get('is_datecreate'),
            'between_datecreate_to':    request.GET.get('between_datecreate_to'),
            'between_datecreate_from':  request.GET.get('between_datecreate_from'),
        }
        rules = searchFirwallRule(rules, search['src_ip'], search['dest_ip'], search['port'], search['description'], search['search_by_date_type'], search['is_datecreate'], search['between_datecreate_from'], search['between_datecreate_to'])

    for rule in rules:
        rule.dest_ip_raw = rule.dest_ip
        rule.dest_ip = rule.dest_ip.split(';')
        rule.port_raw = rule.port
        rule.port = rule.port.split(';')
    if request.GET.get('row'):
        row = request.GET.get('row')
    else:
        row = 10
    paginator = Paginator(rules, row)

    page = request.GET.get('page')

    try:
        firewall_rule = paginator.page(page)
    except PageNotAnInteger:
        firewall_rule = paginator.page(1)
    except EmptyPage:
        firewall_rule = paginator.page(paginator.num_pages)
    return render(request, 'report_firewall_rule.html', {'firewall_rule': firewall_rule,
                                                         'search': search,
                                                         'row' : row})

@login_required
def handleFirewallRule(request):
    if request.FILES.get('myfile', False):
        file = request.FILES['myfile']
        data = get_data(file)
        importFirewallRuleDB(data)
    if request.POST.get('action') == 'del_rule':
        id = request.POST.get('id')
        delFirewallRule(id)
    if request.POST.get('action') == 'edit_rule':
        id = request.POST.get('id')
        rule = {
            'src_ip':       request.POST.get('src_ip'),
            'dest_ip':      request.POST.get('dest_ip'),
            'port':         request.POST.get('port'),
            'description':  request.POST.get('description'),
            'datecreate':   request.POST.get('datecreate')
        }
        editFirewallRule(id, rule)

    return HttpResponseRedirect(reverse('ISCSM:report_firewall_rule'))


@login_required
def network(request):
    if request.method == 'GET' and request.GET.get('action') == 'ping':
        src = request.GET.get('src')
        dest = request.GET.get('dest')

        result = pingHost(src, dest)
        if result['status_code'] == -1:
            data = {
                'result':       str(result['error']),
            }
        elif result['status_code'] and result['result'].std_err:
            data = {
                'result':       result['result'].std_err,
            }
        else:
            data = {
                'result':       result['result'].std_out,
            }
        return JsonResponse(data)

    if request.method == 'GET' and request.GET.get('action') == 'tracert':
        src = request.GET.get('src')
        dest = request.GET.get('dest')
        timeout = request.GET.get('timeout')

        src_validate = validate_ip(src)
        dest_validate = validate_ip(dest)

        if src_validate and dest_validate:
            result = tracerouteHost(src, dest, timeout)
            if result['status_code'] == -1:
                data = {
                    'result':       str(result['error']),
                    'src':          True,
                    'dest':         True,
                }
            elif result['status_code']:
                data = {
                    'result':       result['result'].std_err,
                    'src':          True,
                    'dest':         True,
                }
            else:
                data = {
                    'result':       result['result'].std_out,
                    'src':          True,
                    'dest':         True,
                }
        else:
            data = {
                'src':      src_validate,
                'dest':     dest_validate,
            }
        return JsonResponse(data)

    if request.method == 'GET' and request.GET.get('action') == 'telnet':
        src = request.GET.get('src')
        dest = request.GET.get('dest')
        port = request.GET.get('port')

        src_validate = validate_ip(src)
        dest_validate = validate_ip(dest)
        port_validate = validate_port(port)

        if src_validate and dest_validate and port_validate:
            result = telnet_host(src, dest, port)
            data = {
                'result':       result,
                'src':          True,
                'dest':         True,
                'port':         True,
            }
        else:
            data = {
                'src':      src_validate,
                'dest':     dest_validate,
                'port':     port_validate,
            }

    if request.method == 'GET' and request.GET.get('action') == 'list_int':
        src = request.GET.get('src')

        src_validate = validate_ip(src)

        if src_validate:
            result = tcprouteHost(src, '', request.GET.get('action'))
            if result['status_code'] == -1:
                data = {
                    'result':       str(result['error']),
                    'src':          True,
                }
            elif result['status_code']:
                data = {
                    'result':       result['result'].std_err,
                    'src':          True,
                }
            else:
                data = {
                    'result':       result['result'].std_out,
                    'src':          True,
                }
        else:
            data = {
                'src':          src_validate,
            }
        return JsonResponse(data)

    if request.method == 'GET' and request.GET.get('action') == 'tcproute':
        src = request.GET.get('src')
        dest = request.GET.get('dest')
        port = request.GET.get('port')
        interface = request.GET.get('int')

        src_validate = validate_ip(src)
        dest_validate = validate_ip(dest)
        port_validate = validate_port(port)
        int_validate = validate_port(interface)

        if src_validate and dest_validate and port_validate and int_validate:
            result = tcprouteHost(src, 'tcproute -d -w 200 -h 20 -i %s -p %s %s' % (interface, port, dest), request.GET.get('action'))
            if result['status_code'] == -1:
                data = {
                    'result':       str(result['error']),
                    'src':          True,
                    'dest':         True,
                    'port':         True,
                    'int':          True,
                }
            elif result['status_code']:
                data = {
                    'result':       result['result'].std_err,
                    'src':          True,
                    'dest':         True,
                    'port':         True,
                    'int':          True,
                }
            else:
                data = {
                    'result':       result['result'].std_out,
                    'src':          True,
                    'dest':         True,
                    'port':         True,
                    'int':          True,
                }
        else:
            data = {
                'src':          src_validate,
                'dest':         dest_validate,
                'port':         port_validate,
                'int':          int_validate,
            }
        return JsonResponse(data)

    return render(request, 'network.html')

@login_required
def document(request):
    path = request.GET.get('path')
    if path:
        path = urllib.unquote(path)
    else:
        path = '/'
    listsubdoctype = list(UploadCategory.objects.filter(path=path).order_by('title').values())
    if path != '/':
        traceback = {
            'path':     tracebackCategory(path),
            'name':     'traceback',
            'title':    '--',
        }
        listsubdoctype.insert(0, traceback)

    listdoctype = UploadCategory.objects.filter(path='/').order_by('title')
    listfile = Upload.objects.filter(category=path, del_flag=True)
    if 'result' in request.session:
        result = request.session['result']
        del request.session['result']
    else:
        result = ''

    return render(request, 'simple_upload.html', { 'listfile'       :listfile,
                                                   'listdoctype'    :listdoctype,
                                                   'listsubdoctype' :listsubdoctype,
                                                   'result'         :result,})

@login_required
def handleDocument(request):
    if request.FILES.getlist('myfile', False):
        files = request.FILES.getlist('myfile')
        path = urllib.unquote(request.POST.get('path'))
        request.session['result'] = []

        for myfile in files:
            location = '/media' + path
            filename = myfile.name

            fs = FileSystemStorage(location=location, base_url=path)
            result = uploadFile(filename, fs, myfile, path, request.user.username)
            request.session['result'].append(result)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.GET.get('action') == 'create_category':
        validate = CategoryForm(request.GET)
        if validate.is_valid():
            doctype = validate.cleaned_data['name']
            title = validate.cleaned_data['title']
            path = validate.cleaned_data['path']
            if not title:
                title = doctype
            result = createCategory(doctype, path, title)
            if not result:
                validate.errors['name'] = 'Category existed!'
                return JsonResponse(validate.errors)
        else:
            return JsonResponse(validate.errors)

    if request.GET.get('action') == 'edit_category':
        validate = CategoryForm(request.GET)
        if validate.is_valid():
            old_doctype = request.GET.get('select')
            new_doctype = validate.cleaned_data['name']
            title = validate.cleaned_data['title']
            path = validate.cleaned_data['path']

            if not title:
                title = new_doctype
            result = editCategory(old_doctype, new_doctype, path, title)
            if not result:
                validate.errors['name'] = 'Category existed!'
                return JsonResponse(validate.errors)
        else:
            return JsonResponse(validate.errors)

    if request.GET.get('action') == 'delete':
        id_file_list = request.GET.getlist('list_file')
        id_category_list = request.GET.getlist('list_folder')
        deleteFile(id_file_list)
        deleteCategory(id_category_list)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def radius(request):
    return render(request, 'radius.html')

@login_required
def monitorRadius(request):
    index = request.GET.get('index')
    zone = request.GET.get('zone')
    logfile_name = '[%s]%s_%s' % (request.user.username, zone, index)
    pattern = re.compile('^\[.*\]%s_%s' % (zone, index))
    if request.GET.get('action') == 'play':
        for file in os.listdir('/media/radius_log/'):
            #Continue maintain existed connection
            if pattern.match(file) and pattern.match(file).group() == logfile_name:
                try:
                    data = telnetRadius(zone, index, 'moni')
                    f = open('/media/radius_log/%s' % logfile_name, 'w')
                    f.write(data)
                    f.close()
                except timeout_decorator.timeout_decorator.TimeoutError:
                    data = 'Time out!\r\n'
                return HttpResponse(data)
            #Telnet connection already established:
            elif pattern.match(file):
                f = open('/media/radius_log/%s' % pattern.match(file).group(), 'r')
                data = f.read()
                f.close()
                return HttpResponse(data)
        #First time send request and telnet connection still not exists
        try:
            data = telnetRadius(zone, index, 'moni')
            f = open('/media/radius_log/%s' % logfile_name, 'w')
            f.write(data)
            f.close()
        except timeout_decorator.timeout_decorator.TimeoutError as err:
            data = 'Time out!\n'
        except ZoneNotExist as err:
            data = err
        return HttpResponse(data)

    if request.GET.get('action') == 'show_config':
        data = telnetRadius(zone, index, 'show_config')
        return HttpResponse(data)

    if request.GET.get('action') == 'stop':
        if os.path.isfile('/media/radius_log/%s' % logfile_name):
            os.remove('/media/radius_log/%s' % logfile_name)
        time.sleep(1)
        if os.path.isfile('/media/radius_log/%s' % logfile_name):
            os.remove('/media/radius_log/%s' % logfile_name)
        return HttpResponse('')

    return render(request, 'radius_monitor.html')

@login_required
def logTask(request):
    tasks = Task.objects.all()
    if request.POST.get('action') == 'add_task':
        validate = TaskForm(request.POST)
        if validate.is_valid():
            subject = validate.cleaned_data['subject']
            start_date = validate.cleaned_data['start_date']
            due_date = validate.cleaned_data['due_date']
            done = validate.cleaned_data['done']
            status = validate.cleaned_data['status']
            assignee = validate.cleaned_data['assignee']
            department = validate.cleaned_data['department']
            tracker = validate.cleaned_data['tracker']
            complexity = validate.cleaned_data['complexity']
            estimated_time = validate.cleaned_data['estimated_time']
            spent_time = validate.cleaned_data['spent_time']
            actual_end_date = validate.cleaned_data['actual_end_date']
            project = validate.cleaned_data['project']
            Task.objects.create(subject=subject, start_date=start_date, due_date=due_date, done=done, status=status, assignee=assignee, department=department, tracker=tracker, complexity=complexity, estimated_time=estimated_time, spent_time=spent_time, actual_end_date=actual_end_date, project=project)
        else:
            return render(request, 'log_task.html', {'tasks':   tasks,
                                                     'errors':  validate.errors,
                                                     'task_request': {
                                                        'subject':          request.POST.get('subject'),
                                                        'start_date':       request.POST.get('start_date'),
                                                        'due_date':         request.POST.get('due_date'),
                                                        'done':             request.POST.get('done'),
                                                        'status':           request.POST.get('status'),
                                                        'assignee':         request.POST.get('assignee'),
                                                        'department':       request.POST.get('department'),
                                                        'complexity':       request.POST.get('complexity'),
                                                        'estimated_time':   request.POST.get('estimated_time'),
                                                        'spent_time':       request.POST.get('spent_time'),
                                                        'actual_end_date':  request.POST.get('actual_end_date'),
                                                        'project':          request.POST.get('project'),
                                                     }
                                                    })

    if request.POST.get('action') == 'edit_task':
        validate = TaskForm(request.POST)
        if validate.is_valid():
            id = request.POST.get('id')
            subject = validate.cleaned_data['subject']
            start_date = validate.cleaned_data['start_date']
            due_date = validate.cleaned_data['due_date']
            done = validate.cleaned_data['done']
            status = validate.cleaned_data['status']
            assignee = validate.cleaned_data['assignee']
            department = validate.cleaned_data['department']
            tracker = validate.cleaned_data['tracker']
            complexity = validate.cleaned_data['complexity']
            estimated_time = validate.cleaned_data['estimated_time']
            spent_time = validate.cleaned_data['spent_time']
            actual_end_date = validate.cleaned_data['actual_end_date']
            project = validate.cleaned_data['project']
            Task.objects.filter(id=id).update(subject=subject, start_date=start_date, due_date=due_date, done=done, status=status, assignee=assignee, department=department, tracker=tracker, complexity=complexity, estimated_time=estimated_time, spent_time=spent_time, actual_end_date=actual_end_date, project=project)

    if request.POST.get('action') == 'del_task':
        id = request.POST.get('id')
        Task.objects.filter(id=id).delete()

    return render(request, 'log_task.html', {'tasks': tasks,})

@login_required
def exportTask(request):
    if request.GET.get('assignee'):
        assignee = request.GET.get('assignee')
        assignee_tasks = Task.objects.filter(assignee=assignee).all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="' + assignee + '.csv"'
        response['Content-Type'] = 'application/x-download'

        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['#', 'Subject', 'Start date', 'Due date', '% Done', 'Status', 'Assignee', 'Department', 'Tracker', 'Complexity', 'Estimated time', 'Spent time', 'Actual End Date', 'Project'])
        for task in assignee_tasks:
            writer.writerow(['', task.subject.encode('utf8'), task.start_date.encode('utf8'), task.due_date.encode('utf8'), task.done.encode('utf8'), task.assignee.encode('utf8'), task.department.encode('utf8'), task.tracker.encode('utf8'), task.complexity.encode('utf8'), task.estimated_time.encode('utf8'), task.spent_time.encode('utf8'), task.actual_end_date.encode('utf8'), task.project.encode('utf8')])

    return response
