from __future__ import absolute_import, unicode_literals
import random, winrm, requests
from .models import Zone, ServerInfo
from celery.decorators import task

from ISCSM.utility.web_service import *
from ISCSM.utility.win_service import *

@task()
def test():
    return True

@task()
def scanWebService():
    zone_api_id = Zone.objects.filter(ZoneName='API').get().id
    zone_web_private_id = Zone.objects.filter(ZoneName='Web Private').get().id
    zone_web_public_id = Zone.objects.filter(ZoneName='Web Public').get().id
    zones = [zone_api_id, zone_web_private_id, zone_web_public_id]

    listserver = []
    for zone_id in zones:
        listserver.extend([server.IP for server in ServerInfo.objects.filter(ZoneName_id=zone_id)])

    listservice = []
    for server in listserver:
        tmp_list = []
        result = getIISWebService('%s' % server)
        for x in result.split('\r\n\r\n'):
            service = {}
            if x:
                x = x.split('\r\nphysicalPath')
                for y in x[0].split('\r\n'):
                    if y:
                        tmp = y.replace(' : ','||').split('||')
                        if len(tmp) == 2:
                            if tmp[0].replace(' ','') != 'name':
                                service['%s' % tmp[0].replace(' ','')] = tmp[1] + ';'
                            else:
                                service['%s' % tmp[0].replace(' ','')] = tmp[1]
                service['path'] = x[1].replace(' : ','').replace(' ','').replace('\r\n','')+';'
                service['server'] = server+';'
                tmp_list.append(service.copy())
        if not listservice:
            listservice = tmp_list
        else:
            for tmp_service in tmp_list:
                state = True
                for service in listservice:
                    if service['name'].lower() == tmp_service['name'].lower():
                        service['id'] = service['id']+tmp_service['id']
                        service['server'] = service['server']+tmp_service['server']
                        service['path'] = service['path']+tmp_service['path']
                        service['state'] = service['state']+tmp_service['state']
                        service['enabledProtocols'] = service['enabledProtocols']+tmp_service['enabledProtocols']
                        state = False
                        break
                if state:
                    listservice.append(tmp_service.copy())
    #return listservice
    updateWebServiceDB(listservice)

@task()
def scanWinService():
    listservice = []
    for ip in ['172.20.17.10','172.20.17.11','172.20.17.22','172.20.17.50']:
        tmp_list = []
        result = getUserWinService(ip)
        for x in result.split('\r\n\r\n'):
            service = {}
            if x:
                x = x.split('\r\nstartname')
                for y in x[0].split('\r\n'):
                    if y:
                        tmp = y.split(':')
                        if len(tmp) == 2:
                            if tmp[0].replace(' ','') != 'name':
                                service['%s' % tmp[0].replace(' ','')] = tmp[1] + ';'
                            else:
                                service['%s' % tmp[0].replace(' ','')] = tmp[1]
                service['author'] = x[1].replace(' : ','').replace(' ','').replace('\r\n','')+';'
                service['server'] = ip+';'
                tmp_list.append(service.copy())
        if not listservice:
           listservice = tmp_list
        else:
            for tmp_service in tmp_list:
                state = True
                for service in listservice:
                    if service['name'] == tmp_service['name']:
                        service['server'] = service['server']+tmp_service['server']
                        service['author'] = service['author']+tmp_service['author']
                        service['state'] = service['state']+tmp_service['state']
                        state = False
                        break
                if state:
                    listservice.append(tmp_service.copy())
    updateWinServiceDB(listservice)
