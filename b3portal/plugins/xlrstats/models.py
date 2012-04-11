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

class XlrStatsPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="xlrstats_plugin", unique=True, verbose_name=_('Server'))

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)
    
    class Meta:
        verbose_name = _('XLRStats')
        verbose_name_plural = _('XLRStats')
        db_table = 'plugin_xlrstats'
      
class PlayerStats(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, db_column="client_id", to_field="id", related_name="playerstats")
    kills = models.IntegerField(db_column="kills")
    deaths = models.IntegerField(db_column="deaths")
    teamkills = models.IntegerField(db_column="teamkills")
    teamdeaths = models.IntegerField(db_column="teamdeaths")
    suicides = models.IntegerField(db_column="suicides")
    ratio = models.FloatField(db_column="ratio")
    skill = models.FloatField(db_column="skill")
    assists = models.IntegerField(db_column="assists")
    assistskill = models.FloatField(db_column="assistskill")
    curstreak = models.IntegerField(db_column="curstreak")
    winstreak = models.IntegerField(db_column="winstreak")
    losestreak = models.IntegerField(db_column="losestreak")
    rounds = models.IntegerField(db_column="rounds")
    hide = models.IntegerField(db_column="hide")
    fixed_name = models.CharField(db_column="fixed_name", max_length=32)

    def __unicode__(self):
        return repr(self)
    
    def __repr__(self):
        return "%s: [%s] %s" % (self.id, self.client.id, self.client.name)
    
    class Meta:
        managed = False
        db_table = 'xlr_playerstats'