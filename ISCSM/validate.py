import re

def validate_network_tracert(src, dest):
    ip_format = re.compile('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    validate = {
        'src':   True,
        'dest':  True,
    }
    if not ip_format.match(src):
        validate['src'] = False
    if not ip_format.match(dest):
        validate['dest'] = False

    return validate

def validate_ip(ip):
    ip_format = re.compile('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    if not ip_format.match(ip):
        return False
    return True

def validate_port(port):
    port_format = re.compile('^[0-9]+$')
    if not port_format.match(port):
        return False
    return True
