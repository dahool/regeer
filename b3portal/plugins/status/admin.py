from django.contrib import admin
from models import StatusPlugin
from b3connect.admin import CustomModelAdmin

#class ServerStatusAdmin(CustomModelAdmin):
#    search_fields=['=map']
#    list_filter=('server',)
    
#admin.site.register(ServerStatus, ServerStatusAdmin)

admin.site.register(StatusPlugin)