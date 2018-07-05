import winrm
from ISCSM.models import WebService, Zone, ServerInfo

def updateWebServiceDescript(id, description, ha, author, ip_restrict):
    WebService.objects.filter(id=id).update(description=description, ha=ha, author=author, ip_restrict=ip_restrict)

def searchWebService(listservice, service, server, state, path, protocol, author):
    if service:
        listservice = [services for services in listservice if service in services.service.lower()]
    if server:
        listservice = [services for services in listservice if server in services.server]
    if state:
        listservice = [services for services in listservice if state in services.state.lower()]
    if path:
        listservice = [services for services in listservice if path in services.path.lower()]
    if protocol:
        listservice = [services for services in listservice if protocol in services.protocol.lower()]
    if author:
        listservice = [services for services in listservice if author in services.author.lower()]
    return listservice

def getIISWebService(ip):
    rm_host = winrm.Session( ip, auth=('Administrator', 'Abc@123'))
    script= """Import-Module WebAdministration
    Get-ChildItem -Path IIS:\Sites |Format-List id, name, state, enabledProtocols, physicalPath"""
    result = rm_host.run_ps(script)
    return result.std_out

def updateWebServiceDB(listservice):
    WebService.objects.all().update(del_flag=False)
    existed_services = WebService.objects.all()
    for service in listservice:
        state = True
        if existed_services:
            for existed_service in existed_services:
                if existed_service.service==service['name'] and existed_service.service_id==service['id']:
                    WebService.objects.filter(id=existed_service.id).update(server=service['server'], path=service['path'], state=service['state'], protocol=service['enabledProtocols'], del_flag=True)
                    state = False
                    break
                elif existed_service.service==service['name']:
                    WebService.objects.filter(id=existed_service.id).update(service_id=service['id'], server=service['server'], path=service['path'], state=service['state'], protocol=service['enabledProtocols'], del_flag=True)
                    state = False
                    break
                elif existed_service.service_id==service['id']:
                    WebService.objects.filter(id=existed_service.id).update(service=service['name'], server=service['server'], path=service['path'], state=service['state'], protocol=service['enabledProtocols'], del_flag=True)
                    state = False
                    break
            if state:
                WebService.objects.create(service_id=service['id'], service=service['name'], server=service['server'], path=service['path'], state=service['state'], protocol=service['enabledProtocols'], del_flag=True)
        else:
            WebService.objects.create(service_id=service['id'], service=service['name'], server=service['server'], path=service['path'], state=service['state'], protocol=service['enabledProtocols'], del_flag=True)
    WebService.objects.filter(del_flag=False).delete()
