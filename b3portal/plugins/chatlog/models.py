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
from django.utils.translation import ugettext_lazy as _
from b3connect.models import Client
from b3connect.fields import EpochDateTimeField
from b3portal.models import Server

TEAM_NAME = (
    (0,'-'),
    (-1, _('Everyone')),
    (1, _('Spectator')),
    (2, _('Blue Team')),
    (3, _('Red Team'))
)
             
MSG_TYPE = (
    ('ALL', _('Everyone')),
    ('TEAM', _('Team')),
    ('PM', _('PM'))
)
                              
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
    time_add = EpochDateTimeField(db_index=True, db_column="msg_time")
    type = models.CharField(max_length=5, choices=MSG_TYPE, db_column="msg_type")
    client = models.ForeignKey(Client, db_column="client_id", to_field="id", related_name="chats")
    client_team = models.IntegerField(db_column="client_team",choices=TEAM_NAME)
    message = models.CharField(max_length=528, blank=True, null=True)
    target = models.ForeignKey(Client, db_column="target_id", to_field="id", blank=True, default=0, null=True)
    target_team = models.IntegerField(db_column="target_team",choices=TEAM_NAME, null=True, default=0)
    
    def __unicode__(self):
        return repr(self)
    
    def __repr__(self):
        return "%s: %s" % (self.client.name, self.message)
    
    class Meta:
        managed = False
        ordering = ('-time_add',)
        db_table = 'chatlog'
