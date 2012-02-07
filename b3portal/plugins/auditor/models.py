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
from b3connect.models import Client
from b3connect.fields import EpochDateTimeField
from b3portal.models import Server
from django.utils.translation import gettext_lazy as _

class AuditLogPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="auditor_plugin", unique=True, verbose_name=_('Server'))

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)
    
    class Meta:
        verbose_name = _('Auditor')
        verbose_name_plural = _('Auditor')
        db_table = 'plugin_auditor'   
            
class AuditLog(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client,
                               db_column="client_id",
                               to_field="id",
                               related_name="commands")
    target = models.ForeignKey(Client,
                               db_column="target_id",
                               to_field="id",
                               related_name="admin_logs",
                               blank=True, default=0, null=True)
    command = models.CharField(max_length=20)    
    data = models.CharField(max_length=50, blank=True, null=True)
    time_add = EpochDateTimeField()
    
    def __unicode__(self):
        return u"%s" % self.command
        
    def __repr__(self):
        return str(self)
        
    class Meta:
        managed = False
        verbose_name_plural = "Audits"
        ordering = ('-time_add',)
        db_table = u'auditlog'