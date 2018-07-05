import telnetlib, time
import timeout_decorator

class error(Exception):
    pass

class ZoneNotExist(error):
    pass

@timeout_decorator.timeout(1, use_signals=False)
def telnetRadius(zone, index, cmd):
    if zone in ['HCM', 'HNI', 'CAM']:
        if zone == 'HCM':
            telnet = telnetlib.Telnet("118.69.241.%s" % index)
        elif zone == 'HNI':
            telnet = telnetlib.Telnet("210.245.0.%s" % index)
        elif zone == 'CAM':
            telnet = telnetlib.Telnet("202.58.98.%s" % index)
        try:
            telnet.read_until('Password: ')
            telnet.write('p\r\n')
            if cmd == 'moni':
                telnet.write('moni\r\n')
                time.sleep(0.45)
                telnet.read_until('Press Enter to stop\r\n\r\n')
                data = telnet.read_very_eager()
            if cmd == 'show_config':
                telnet.write('show config\r\n')
                telnet.write('\r\n\r\n')
                telnet.write('exit\r\n')
                data = telnet.read_all()
            telnet.close()

        except EOFError as err:
            data = str(err) + '\n'
        return data
    raise ZoneNotExist("Zone doesn't exist!\n")
