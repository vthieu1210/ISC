from django.contrib import admin 
from .models import Zone, ServerInfo, Switch, Firewall, Service, Location




class Serviceline(admin.StackedInline):
   	model = Service
   	extra = 0 

class Locationline(admin.StackedInline):
   	model = Location
   	max_num = 1
   	  	
class Switchline(admin.StackedInline):
   	model = Switch
   	extra = 0
 # 	max_num=1

class FirewallInline(admin.StackedInline):
    model = Firewall
    extra = 0

class SVAdmin(admin.ModelAdmin):
    inlines = [Locationline,Serviceline,Switchline,FirewallInline]
    list_display = ['IP','ServerName','ServerType','Function']
    search_fields = ['IP','ServerName']


admin.site.register(ServerInfo, SVAdmin)
admin.site.register(Zone)

