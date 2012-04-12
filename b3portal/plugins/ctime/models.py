# -*- coding: utf-8 -*-
"""Copyright (c) 2012 Sergio Gabriel Teves
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
from django.utils.translation import gettext_lazy as _
from b3portal.models import Server
from b3connect.models import Client

class CtimePlugin(models.Model):
    server = models.ForeignKey(Server, related_name="ctime_plugin", unique=True, verbose_name=_('Server'))

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)
    
    class Meta:
        verbose_name = _('CTime')
        verbose_name_plural = _('CTime')
        db_table = 'plugin_ctime'
      
class ClientTime(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, db_column="guid", to_field="guid", related_name="playtime")
    guid = models.CharField(db_column="guid", max_length=36)
    came = models.CharField(db_column="came", max_length=11)
    gone = models.CharField(db_column="gone", max_length=11)
    nick = models.CharField(db_column="nick", max_length=32)

    def __unicode__(self):
        return repr(self)
    
    def __repr__(self):
        return "[%s] %s" % (self.client.id, self.client.name)
    
    @property
    def start(self):
        return long(self.came)
    
    @property
    def end(self):
        return long(self.gone)
    
    class Meta:
        managed = False
        db_table = 'ctime'