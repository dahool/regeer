from django.contrib import admin
from b3connect.admin import CustomModelAdmin
from django.conf import settings
from b3portal.plugins.status.models import StatusPlugin, ServerStatus, StatusClient

#class ServerStatusAdmin(CustomModelAdmin):
#    search_fields=['=map']
#    list_filter=('server',)
    
#admin.site.register(ServerStatus, ServerStatusAdmin)

if settings.DEBUG:
    admin.site.register(ServerStatus)
    admin.site.register(StatusClient)
        
admin.site.register(StatusPlugin)