from django.contrib import admin
from .models import Zone, ServerInfo, Switch, Service, Location

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

class SVAdmin(admin.ModelAdmin):
    inlines = [Locationline,Serviceline,Switchline]
    list_display = ['IP','ServerName','ServerType','Function']
    search_fields = ['IP','ServerName']


admin.site.register(ServerInfo, SVAdmin)
admin.site.register(Zone)
