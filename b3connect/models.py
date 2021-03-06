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
import hashlib as hash
import time, datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from common.utils.functions import duration_human
from django.db.models import Q

from b3connect.fields import EpochDateTimeField

class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    keyword = models.CharField(unique=True, max_length=32, blank=True)
    level = models.IntegerField(blank=True, default=0)
    time_edit = EpochDateTimeField()
    time_add = EpochDateTimeField()

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return ("%s (Level %d)") % (self.name, self.level)
    
    class Meta:
        managed = False
        ordering  = ('id',)
        db_table = u'groups'
                
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=16)
    connections = models.IntegerField()
    guid = models.CharField(unique=True, max_length=36)
    pbid = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=32)
    auto_login = models.IntegerField()
    mask_level = models.IntegerField()
    group = models.ForeignKey(Group, to_field="id", db_column="group_bits", default=0, null=True, blank=True)
    greeting = models.CharField(max_length=128, blank=True)
    login = models.CharField(max_length=16, blank=True)
    password = models.CharField(max_length=32, blank=True)
    time_edit = EpochDateTimeField()
    time_add = EpochDateTimeField()

    def __unicode__(self):
        return repr(self)
    
    def __repr__(self):
        if self.group_id > 0:
            return "%s - %s (%s)" % (self.id, self.name, self.group.name)
        else:
            return "%s - %s" % (self.id, self.name)
        
    @property
    def displayGroup(self):
        if self.group:
            return self.group
        else:
            return _('Guest')
        
    @property
    def masked_ip(self):
        ips = self.ip.split(".")
        return ".".join(ips[:-1]) + ".XXX"
    
    def check_password(self, password):
        if self.password == '':
            return False
        return self.password == hash.md5(password).hexdigest()
        
    class Meta:
        managed = False
        ordering = ('id',)
        db_table = u'clients'

class Alias(models.Model):
    id = models.AutoField(primary_key=True)
    num_used = models.IntegerField()
    alias = models.CharField(unique=True, max_length=32)
    client = models.ForeignKey(Client, db_column="client_id", related_name="aliases", to_field="id")
    time_edit = EpochDateTimeField()
    time_add = EpochDateTimeField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s [%s] - [%s]" % (self.client.name,self.alias, self.ip)
        
    class Meta:
        managed = False
        ordering = ('-time_edit',)
        verbose_name_plural = "Aliases"
        db_table = u'aliases'

class AliasIP(models.Model):
    id = models.AutoField(primary_key=True)
    num_used = models.IntegerField()
    ip = models.CharField(max_length=32, blank=True, null=True)
    client = models.ForeignKey(Client, db_column="client_id", related_name="ip_aliases", to_field="id")
    time_edit = EpochDateTimeField()
    time_add = EpochDateTimeField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s [%s] - [%s]" % (self.client.name,self.alias, self.ip)
        
    class Meta:
        managed = False
        ordering = ('-time_edit',)
        verbose_name_plural = "IP Aliases"
        db_table = u'ipaliases'

PENALTY_TYPE_NOTICE = 'Notice'
PENALTY_TYPE_WARN = 'Warning'       
PENALTY_TYPE_BAN = 'Ban'
PENALTY_TYPE_TEMPBAN = 'TempBan'
PENALTY_TYPE_KICK = 'Kick'

TYPE_COMMENT = 'NOTE'

PENALTY_CHOICES = (
    (PENALTY_TYPE_WARN, _('Warning')),
    (PENALTY_TYPE_NOTICE, _('Notice')),
    (PENALTY_TYPE_BAN, _('Ban')),
    (PENALTY_TYPE_TEMPBAN, _('TempBan')),
    (PENALTY_TYPE_KICK, _('Kick')),
)

class PenaltyManager(models.Manager):
    
    def comments(self):
        return self.filter(keyword=TYPE_COMMENT).order_by('-time_add')
    
    def active(self):
        return self.filter(Q(time_expire='-1') | Q(time_expire__gt=int(time.time())),inactive=0)

    def active_bans(self):
        return self.filter(Q(time_expire='-1') | Q(time_expire__gt=int(time.time())),
                    (Q(type=PENALTY_TYPE_BAN) | Q(type=PENALTY_TYPE_TEMPBAN)),inactive=0)

    def notices(self):
        return self.filter(type=PENALTY_TYPE_NOTICE,inactive=0)
        
    def inactive(self):
        return self.filter(Q(inactive=1) | 
                           Q(time_expire__lt=int(time.time())) & ~Q(type=PENALTY_TYPE_NOTICE)
                           ).exclude(Q(inactive=0) & Q(time_expire='-1'))
        
    def noexpired(self):
        return self.filter(Q(time_expire='-1') | Q(time_expire__gt=int(time.time())))
    
class Penalty(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=21, choices=PENALTY_CHOICES)
    client = models.ForeignKey(Client, db_column="client_id", related_name="penalties", to_field="id")
    admin = models.ForeignKey(Client, db_column="admin_id", to_field="id", blank=True, default=0, null=True, related_name="adminpenalties")
    duration = models.IntegerField()
    inactive = models.IntegerField(default=0)
    keyword = models.CharField(max_length=16, blank=True,default='')
    reason = models.CharField(max_length=255)
    data = models.CharField(max_length=255, blank=True, default='')
    time_edit = EpochDateTimeField()
    time_add = EpochDateTimeField()
    time_expire = EpochDateTimeField(blank=True)

    objects = PenaltyManager()
    
    def __unicode__(self):
        if self.duration == 0:
            return ugettext(u"%(type)s: %(reason)s" % {'type': self.get_type_display(), 'reason': self.reason})
        return ugettext(u"%(type)s: %(reason)s. Duration: %(duration)s" % {'type': self.get_type_display(),
                                                                    'duration': self.display_duration,
                                                                    'reason': self.reason})
            
    def __repr__(self):
        return "%s - %s [%s] (%s)" % (self.client.name,
                                      self.type,
                                      self.reason,
                                      self.time_add.strftime("%d/%m/%Y %H:%M"))
    
    class Meta:
        managed = False
        ordering = ('-time_add',)
        verbose_name_plural = "Penalties"
        db_table = u'penalties'
        get_latest_by = "time_add"
        
    @property
    def display_duration(self):
        if self.duration > 0:
            return duration_human(self.duration*60)
        return ''
    
    @property
    def display_data(self):
        if self.data and not self.data.startswith("UP#"):
            return self.data
        return None
    
    @property
    def admin_username(self):
        if self.data and self.data.startswith("UP#"):
            return "@" + self.data[3:]
        return None
    
    @property
    def is_expired(self):
        return self.time_expire < datetime.datetime.now()
        
    def save(self, *args, **kwargs):
        if self.duration == 0 and self.type == PENALTY_TYPE_BAN:
            self.time_expire = -1
        else:
            self.time_expire =  int(time.mktime(self.time_add.timetuple())) + (self.duration * 60)
        super(Penalty, self).save(*args, **kwargs)
        
#class Nick(models.Model):
#    nickid = models.IntegerField(db_index=True)
#    name = models.CharField(unique=True, max_length=32)
#    client = models.ForeignKey(Client, db_column="clientid", related_name="nicks", to_field="id")
#    time_add = EpochDateTimeField()
#    
#    def __unicode__(self):
#        return repr(self)
#        
#    def __repr__(self):
#        return "%s [%s]" % (self.client.name,self.name)
#        
#    class Meta:
#        ordering = ('client',)
#        verbose_name_plural = "Nicks"
#        db_table = u'nicks'
#        
#class DisabledCommand(models.Model):
#    id = models.AutoField(primary_key=True)
#    cmd = models.CharField(unique=True, max_length=50)
#    until = EpochDateTimeField()
#    
#    def __unicode__(self):
#        return repr(self)
#        
#    def __repr__(self):
#        return "%s [%s]" % (self.cmd,self.until)
#        
#    class Meta:
#        db_table = u'disabledcmd'
#        
#class AuditLog(models.Model):
#    id = models.AutoField(primary_key=True)
#    client = models.ForeignKey(Client, db_column="client_id", to_field="id", related_name="commands")
#    command = models.CharField(max_length=20, db_index=True)
#    data = models.CharField(max_length=50, blank=True, null=True)
#    time_add = EpochDateTimeField(db_index=True)
#    
#    def __unicode__(self):
#        return repr(self)
#    
#    def __repr__(self):
#        return "%s: %s" % (self.client.name, self.command)
#    
#    class Meta:
#        ordering = ('-time_add',)
#        db_table = u"auditlog"