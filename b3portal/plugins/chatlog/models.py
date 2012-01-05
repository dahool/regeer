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
from django.db import models
from django.utils.translation import ugettext_lazy as _
from b3connect.models import Client
from b3connect.fields import EpochDateTimeField
from b3portal.models import Server

CHAT_TARGETS = {'ALL': _('Everyone'),
                'TEAM: BLUE': _('Blue Team'),
                'TEAM: RED': _('Red Team')}

class ChatLogPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="chatlog_plugin", unique=True, verbose_name=_('Server'))

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)

    class Meta:
        verbose_name = _('Chat Log')
        verbose_name_plural = _('Chat Log')
        db_table = 'plugin_chatlog'   
        
class ChatLog(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, db_column="client_id", to_field="id", related_name="chats")
    data = models.CharField(max_length=100, blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)
    target = models.CharField(max_length=50, blank=True, null=True)
    time_add = EpochDateTimeField(db_index=True)
    
    def __unicode__(self):
        return repr(self)
    
    def __repr__(self):
        return "%s: %s" % (self.client.name, self.data)
    
    @property
    def target_display(self):
        return CHAT_TARGETS.get(self.target,self.target)
    
    class Meta:
        managed = False
        ordering = ('-time_add',)
        db_table = u"chatlog"
        permissions = (
            ("view_chat", "View chat logs"),
        )