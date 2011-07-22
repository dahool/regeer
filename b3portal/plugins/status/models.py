# -*- coding: utf-8 -*-
"""Copyright (c) 2011 Sergio Gabriel Teves
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
from b3portal.models import Server
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django.core.files.base import ContentFile

from b3portal.plugins.status.element import Status

import datetime

class StatusPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="status_plugin", unique=True, verbose_name=_('Server'))
    location = models.CharField(max_length=500, verbose_name=_('Status File Location'),
                                help_text=_('For ftp access use: ftp://user:password@host:port/file/status.xml'))
    cache = models.FileField(upload_to='status', max_length=500, editable=False, null=True)
    updated = models.DateTimeField(editable=False, null=True)
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)
    
    def get_status(self):
        d = datetime.timedelta(minutes=getattr(settings, 'PLUGIN_STATUS_EXPIRE', 1))
        if not self.cache or not self.updated or self.updated + d < datetime.datetime.now():
            from common.utils.file import getfile
            f = getfile(self.location)
            if not f: raise Exception(_('Unable to read status file'))
            if self.location.startswith("ftp://"):
                file_content = ContentFile(f.read())
                f.seek(0)
                self.updated = datetime.datetime.now()
                if self.cache: self.cache.delete()
                self.cache.save(self.server.uuid + ".xml", file_content)
                self.save()
            else:
                return Status(f)
        return Status(self.cache)
        
    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Status')
        db_table = 'plugin_status'
        
class ServerStatus(models.Model):
    server = models.ForeignKey(Server)
    map = models.CharField(max_length=100, db_index=True)
    time_add = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s - %s - %d" % (str(self.server), str(self.time_add), self.totalPlayers)
    
    @property
    def totalPlayers(self):
        return self.players.count()
    
    def is_online(self, client_id):
        for c in self.players.all():
            if c.client_id == client_id:
                return True
        return False
    
    class Meta:
        ordering = ('-time_add',)
        get_latest_by = ('time_add',)
        permissions = (
            ("view_serverstatus", "View Server Status"),
        )
        
class StatusClient(models.Model):
    status = models.ForeignKey(ServerStatus, related_name='players')
    client_id = models.IntegerField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s - %s" % (str(self.status), self.client_id)
    
    @property
    def client(self):
        return Client.objects.using(self.status.server.uuid).get(pk=self.client_id)