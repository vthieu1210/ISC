import winrm, re
from ISCSM.models import WinService, Zone, ServerInfo

def updateWinServiceDescript(id, description):
    WinService.objects.filter(id=id).update(description=description)

def searchWinService(listservice, service, server, state, author, type):
    if service:
        listservice = [services for services in listservice if service in services.service.lower()]
    if server:
        listservice = [services for services in listservice if server in services.server]
    if state:
        listservice = [services for services in listservice if state in services.state.lower()]
    if author:
        listservice = [services for services in listservice if author in services.author.lower()]
    if type == 'local':
        tmp = []
        regex = re.compile('.*local|AUTHORITY|NT.*', re.IGNORECASE)
        for services in listservice:
            if regex.match(services.author):
                tmp.append(services)
        listservice = tmp
    if type == 'login':
        tmp = []
        regex = re.compile('^((?!local|AUTHORITY|NT).)*$', re.IGNORECASE)
        for services in listservice:
            if regex.match(services.author):
                tmp.append(services)
        listservice = tmp
    return listservice

def getUserWinService(ip):
    rm_host = winrm.Session( ip, auth=('Administrator', 'Abc@123'))
    script= 'Get-WmiObject win32_service | Format-list name, state, startname'
    result = rm_host.run_ps(script)
    return result.std_out

def updateWinServiceDB(listservice):
    WinService.objects.all().update(del_flag=False)
    existed_services = WinService.objects.all()
    for service in listservice:
        state = True
        if existed_services:
            for existed_service in existed_services:
                if existed_service.service==service['name']:
                    WinService.objects.filter(id=existed_service.id).update(server=service['server'], author=service['author'], state=service['state'], del_flag=True)
        else:
            WinService.objects.create(service=service['name'], server=service['server'], author=service['author'], state=service['state'], del_flag=True)
    WinService.objects.filter(del_flag=False).delete()
