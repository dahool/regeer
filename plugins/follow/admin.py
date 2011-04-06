from django.contrib import admin
from models import Follow
from b3connect.admin import CustomModelAdmin

class FollowAdmin(CustomModelAdmin):
    search_fields=['=client__id','client__name']
    raw_id_fields=('client','admin')
    
admin.site.register(Follow, FollowAdmin)