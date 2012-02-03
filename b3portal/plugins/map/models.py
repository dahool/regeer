# -*- coding: utf-8 -*-
"""Copyright (c) 2010,2011 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from django.conf import settings
from django.db import models
from b3portal.models import Server
from django.utils.translation import gettext_lazy as _

import re

DISPLAY_SUB = re.compile(r'ut4_|ut_|ut42_')

class MapPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="map_plugin", unique=True, verbose_name=_('Server'))
    location = models.CharField(max_length=500, verbose_name=_('Mapcycle file location'),
                                help_text=_('Local, ftp and http are supported<br/>For ftp use: ftp://user:password@host:port/file/mapcycle.txt<br/>For http use: http://your.url.com/mapcycle.txt')
                                )

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