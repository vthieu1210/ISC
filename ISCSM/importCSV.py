# -*- coding: utf-8 -*-
#import csv as csv
from models import Zone,ServerInfo,Service,Location,Switch,Upload
from xlrd import *


def ReadFileCSV(filecsv):
	book = open_workbook(file_contents = filecsv.read(), on_demand = True)
#	first_sheet = book.sheet_by_index(0)
#	ass = first_sheet.row_values(1)
#	ddd = first_sheet.cell(1,4)
	return book


def SaveZone(lst):
	try:
		logok=''
		logero=''
		first_sheet = lst.sheet_by_index(0)
		for r in range(1, first_sheet.nrows):
			m 	= first_sheet.cell(r,0).value
			m2 	= first_sheet.cell(r,2).value
			chk 	= Zone.objects.filter(ZoneName=m, Network=m2).exists()
			if chk == False:
				sv=Zone(
					ZoneName 		= m,
					Description 	= first_sheet.cell(r,1).value,
					Network 		= m2,
					)
				sv.save()
				logok += m.encode("utf-8")+'/'
			elif chk == True:
				logero += m.encode("utf-8")+'/'

		return {'y0':logok, 'y1':logero}
	except:
		return False

def SaveServerInfo(lst):
	try:
		logok=''
		logero=''
		first_sheet = lst.sheet_by_index(0)
		for r in range(1, first_sheet.nrows):
			m		= first_sheet.cell(r,2).value
			chk 	= ServerInfo.objects.filter(IP=m).exists()
			if chk == False:
				zone = Zone.objects.get(ZoneName=first_sheet.cell(r,1).value)
				sv=ServerInfo(
					ServerName		= first_sheet.cell(r,0).value,
					ZoneName_id		= zone.id,
					IP 				= first_sheet.cell(r,2).value,
					OS 				= first_sheet.cell(r,3).value,
					OS_Name 		= first_sheet.cell(r,4).value,
	 				Function 		= first_sheet.cell(r,5).value,
					ServerType 		= first_sheet.cell(r,6).value,
					CPU 			= first_sheet.cell(r,7).value,
					RAM 			= first_sheet.cell(r,8).value,
					HDD 			= first_sheet.cell(r,9).value,
					Link_Monitor 	= first_sheet.cell(r,10).value,
					Description 	= first_sheet.cell(r,11).value,
					)
				sv.save()
				logok += m.encode("utf-8")+'/'
			elif chk == True:
				logero += m.encode("utf-8")+'/'

		return {'y0':logok, 'y1':logero}
	except:
		return False


def SaveLocation(lst):
	try:
		logok=''
		logero=''
		first_sheet = lst.sheet_by_index(0)
		for r in range(1, first_sheet.nrows):
			m 		= ServerInfo.objects.get(IP=first_sheet.cell(r,3).value).id
			chk 	= Location.objects.filter(Server_id=m).exists()
			if chk == False:
				sv=Location(
					LocationName 	= first_sheet.cell(r,0).value,
					Rack 			= first_sheet.cell(r,1).value,
					Unit 			= first_sheet.cell(r,2).value,
					Server_id		= m,
					)
				sv.save()
				logok += first_sheet.cell(r,3).value.encode("utf-8")+'/'
			elif chk == True:
				logero += first_sheet.cell(r,3).value.encode("utf-8")+'/'

		return {'y0':logok, 'y1':logero}
	except:
		return False


def SaveSwitch(lst):
	try:
		logok=''
		logero=''
		first_sheet = lst.sheet_by_index(0)
		for r in range(1, first_sheet.nrows):
			m 		= ServerInfo.objects.get(IP=first_sheet.cell(r,4).value).id
			chk 	= Switch.objects.filter(Server_id=m).exists()
			if chk == False:
				sv=Switch(
					SwitchIP 		= first_sheet.cell(r,0).value,
					SwitchType 		= first_sheet.cell(r,1).value,
					SwitchPort 		= first_sheet.cell(r,2).value,
					SwitchLocation	= first_sheet.cell(r,3).value,
					Server_id		= m,
					)
				sv.save()
				logok += first_sheet.cell(r,4).value.encode("utf-8")+'/'
			elif chk == True:
				logero += first_sheet.cell(r,4).value.encode("utf-8")+'/'

		return {'y0':logok, 'y1':logero}
	except:
		return False

def SaveService(lst):
	try:
		logok=''
		logero=''
		first_sheet = lst.sheet_by_index(0)
		for r in range(1, first_sheet.nrows):
			m 	= first_sheet.cell(r,0).value
			m1 	= ServerInfo.objects.get(IP=first_sheet.cell(r,8).value).id
			chk 	= Service.objects.filter(ServiceName=m, Server_id=m1).exists()
#			chkip 	= Service.objects.filter(Server_id = m1).exists()
#			Service.objects.filter(ServiceName=request.POST['name'], Server_id=request.POST['title']).exists()
			if chk == False:
				server = ServerInfo.objects.get(IP=first_sheet.cell(r,8).value)
				sv=Service(
						ServiceName = m,
						ServiceType = first_sheet.cell(r,1).value,
						URL 		= first_sheet.cell(r,2).value,
						RunningAs 	= first_sheet.cell(r,3).value,
						Description = first_sheet.cell(r,4).value,
						URLWEBS 	= first_sheet.cell(r,5).value,
						Header 		= first_sheet.cell(r,6).value,
						Body 		= first_sheet.cell(r,7).value,
						DateCreate 	= first_sheet.cell(r,9).value,
						Owner 		= first_sheet.cell(r,10).value,
						Server_id 	= server.id,
						)
				sv.save()
				logok += first_sheet.cell(r,0).value.encode("utf-8")+'/'
			elif chk == True:
				logero += first_sheet.cell(r,0).value.encode("utf-8")+'/'

#		for svc in lst:
#			server = ServerInfo.objects.get(IP=svc['Server_IP'])
#			sv=Service(
#				ServiceName = svc['ServiceName'],
#				ServiceType = svc['ServiceType'],
#				Description = debug,
#				)
#			sv.save()
		return {'y0':logok, 'y1':logero}
	except:
		return False

def SaveDoc(uploaded_file_url,dateup):
	try:
		sv=Upload(
			pic = uploaded_file_url,
			upload_date = dateup,
			)
		sv.save()
		return True
	except:
		return False
