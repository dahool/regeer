from django.conf import settings
from django.db import models
from b3portal.models import Server
from django.utils.translation import gettext_lazy as _

import re

DISPLAY_SUB = re.compile(r'ut4_|ut_|ut42_')

class MapPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="map_plugin", unique=True, verbose_name=_('Server'))
    location = models.CharField(max_length=500, verbose_name=_('Mapcycle file location'))

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)
    
    class Meta:
        verbose_name = _('Map')
        verbose_name_plural = _('Map')
        db_table = 'plugin_map'            
            
class Map(models.Model):
    server = models.ForeignKey(Server, related_name="maps")
    name = models.CharField(max_length=50)
    
    @property
    def display_name(self):
        return DISPLAY_SUB.sub('',self.name).strip().title() 
    
    @property
    def map_image(self):
        return settings.MAP_IMAGE_URL % self.name
    
    @property
    def map_link(self):
        if not self.name in settings.SKIP_MAPS:
            if settings.MAP_LOCATION:
                return settings.MAP_LOCATION % self.name
        return None
        
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering  = ('server','name')