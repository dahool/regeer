# -*- coding: utf-8 -*-
"""Copyright (c) 2010-2012 Sergio Gabriel Teves
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
from django.db import models
from b3portal.models import Server
from django.utils.translation import gettext_lazy as _

class IpdbPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="ipdb_plugin", unique=True, verbose_name=_('Server'))
    serverKey = models.CharField(max_length=100)
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)
    
    class Meta:
        verbose_name = _('Ipdb')
        verbose_name_plural = _('Ipdb')
        db_table = 'plugin_ipdb'   
            