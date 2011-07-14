from django.contrib import admin
from django.conf import settings
from b3portal.plugins.map.models import MapPlugin, Map
    
if settings.DEBUG:
    admin.site.register(Map)    
admin.site.register(MapPlugin)