from django.contrib import admin
from models import AutoSlap
from b3connect.admin import CustomModelAdmin

class AutoSlapAdmin(CustomModelAdmin):
    search_fields=['=client__id','client__name']
    raw_id_fields=('client','admin')
    
admin.site.register(AutoSlap, AutoSlapAdmin)