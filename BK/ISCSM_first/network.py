import os
import sys
import subprocess
import telnetlib
import winrm
import requests
import ast

def verify_host(host):
    cmd = "ping -c 3 -W 5 %s" % host
    if os.system(cmd):        
   		return "Ping Failed"
    return 'Ping Success'

def traceroute_host(host):
	batcmd="traceroute %s" %host
	result = subprocess.check_output(batcmd, shell=True)
	return result

def telnet_host(host,port):
	try:
		telnetlib.Telnet(host,port,3)
		return 'Telnet Success'
    
	except:
		return 'Telnet Failed'

def status_service(ip):
	connect = winrm.Session( ip, auth=('userwinrm', 'U$erwinrm'))
	runscript = connect.run_ps('Get-WmiObject win32_service | Format-list name, state, startname')
	result = runscript.std_out
	lst=[]
	dic={}
	for a in result.split('\r\n\r\n'):
		if a != '':
			dic=dict(x.split(':') for x in a.split('\r\n'))
			for key in dic.keys():
				dic[key.replace(' ','')]=dic.pop(key)
			lst.append(dic)
	return lst


def winservice_owner(ip):
	connect = winrm.Session( ip, auth=('userwinrm', 'U$erwinrm'))
	runscript = connect.run_ps('Get-WmiObject win32_service |  Where-Object {$_.startname -notlike "LocalSystem"} | Where-Object {$_.startname -notlike "NT*"} |Format-list name, state, startname')
	result = runscript.std_out
	lst=[]
	dic={}
	for a in result.split('\r\n\r\n'):
		if a != '':
			dic=dict(x.split(':') for x in a.split('\r\n'))
			for key in dic.keys():
				dic[key.replace(' ','')]=dic.pop(key)
			lst.append(dic)
	return lst


def eventviewer(ip, check): 
	connect = winrm.Session( ip, auth=('userwinrm', 'U$erwinrm'))
	if check =='app': 
		#runscript = connect.run_ps('Get-EventLog -LogName Application -After (Get-Date).AddDays(-1) -EntryType Error,Warning |Format-List EventID, EntryType, TimeGenerated, Source, Message')
		runscript = connect.run_ps('Get-EventLog Application -newest 50 -EntryType Error,Warning |Format-List EventID, EntryType, TimeGenerated, Source, Message')
	else:
		runscript = connect.run_ps('Get-EventLog -LogName System -newest 50 -EntryType Error,Warning |Format-List EventID, EntryType, TimeGenerated, Source, Message')
	
	result = runscript.std_out
	return result



def check_web(urls,datas,head):
	convert_head=ast.literal_eval(head)
	convert_data=ast.literal_eval(datas)
	
	respone=requests.post(urls,data=convert_data,headers=convert_head)
	return respone.content

def get_info_server(ip):
	lst={}
	connect = winrm.Session( ip, auth=('userwinrm', 'U$erwinrm'))
	Server_Name = connect.run_ps('(Get-WmiObject Win32_ComputerSystem).Name')
	HDH= connect.run_ps('(Get-WmiObject Win32_OperatingSystem).Caption')
	Server_type = connect.run_ps('(Get-WmiObject Win32_ComputerSystem).Model')
	RAM = connect.run_ps('((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory /1Gb).ToString(".00")')
	CPU = connect.run_ps('(Get-WmiObject Win32_Processor | where-object {$_.DeviceID -eq "CPU0"}|Format-List Name)')
	#CPU = connect.run_cmd('wmic cpu get Name /Format:List')
	#CPU = connect.run_ps('(Get-WmiObject Win32_ComputerSystem).Name')
	HDD = connect.run_ps('((Get-WmiObject Win32_LogicalDisk -Filter "DriveType=3" | Measure-Object Size -Sum | Select-Object Sum).Sum /1Gb).ToString(".00")')
	lst={
		'ServerName'	: Server_Name.std_out,
		'OS_Name'		: HDH.std_out,
		'ServerType'	: Server_type.std_out,
		'RAM'			: RAM.std_out,
		'CPU'			: CPU.std_out,
		'HDD'			: HDD.std_out,
	}
	return lst


def IIS_info(ip): 
	connect = winrm.Session( ip, auth=('userwinrm', 'U$erwinrm'))
	script= """Import-Module WebAdministration
	Get-ChildItem -Path IIS:\Sites |Format-List name, state, applicationPool"""
	runscript = connect.run_ps(script)
	result = runscript.std_out
	lst=[]
	dic={}
	for a in result.split('\r\n\r\n'):
		if a != '':
			dic=dict(x.split(':') for x in a.split('\r\n'))
			for key in dic.keys():
				dic[key.replace(' ','')]=dic.pop(key)
			lst.append(dic)
	return lst



