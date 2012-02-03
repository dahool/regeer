# -*- coding: utf-8 -*-
"""Copyright (c) 2011-2012 Sergio Gabriel Teves
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
from django.utils.translation import gettext_lazy as _

from common.fields import CryptField, AutoSlugField, RemoteCachedFileField
import re

from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType
from b3portal import appsettings

DISPLAY_SUB = re.compile(r'ut4_|ut_|ut42_')

DB_ENGINES_CHOICES = (
    ('django.db.backends.mysql', 'mysql'),
#    ('django.db.backends.postgresql', 'postgresql'),
#    ('django.db.backends.postgresql_psycopg2','postgresql_psycopg2'),
#    ('django.db.backends.sqlite3','sqlite3'),
#    ('django.db.backends.oracle','oracle')
)

PARSER_CHOICES = [(v,v) for v in settings.B3_PARSERS]

class Server(models.Model):
    uuid = AutoSlugField(max_length=50, unique=True, editable=False,prepopulate_from="name", force_update=False, primary_key=True)
    name = models.CharField(max_length=40, verbose_name=_('Server Name'), db_index=True)
    game = models.CharField(max_length=15, choices=PARSER_CHOICES, verbose_name=_('Game'))
    default = models.BooleanField(default=False, verbose_name=_('Default'), help_text=_('Set as default server'), db_index=True)
    
    owners = models.ManyToManyField(User, verbose_name=_('Server Owners'), blank=True, related_name="owned_servers")
    
    # database
    database = models.CharField(max_length=50, verbose_name=_('Database Name'))
    engine = models.CharField(max_length=100, choices=DB_ENGINES_CHOICES, verbose_name=_('Database Engine'), editable=False, default='django.db.backends.mysql')
    user = models.CharField(max_length=50, verbose_name=_('Database User'))
    password = CryptField(max_length=200)
    hostname = models.CharField(max_length=50, verbose_name=_('Database Host'))
    
    #rcon
    rcon_ip = models.IPAddressField(verbose_name=_('IP'), blank=True)
    rcon_port = models.IntegerField(verbose_name=_('Port'), blank=True, null=True)
    rcon_password = CryptField(max_length=50, verbose_name=_('RCON Password'), blank=True)
        
    def __repr__(self):
        return self.name
    
    def __unicode__(self):
        return repr(self)
        
    def is_owner(self, user):
        return user in self.owners.all()

    class Meta:
        ordering  = ('name',)
        unique_together = ('database','user','hostname')

class ServerBanList(models.Model):
    server = models.ForeignKey(Server, related_name="banlist", unique=True, verbose_name=_('Server'))
    location = RemoteCachedFileField(max_length=500,
                                     cache_time=getattr(settings, 'BANLIST_CACHE_EXPIRE', 1440),
                                     upload_to='banlist') 
        
    def get_file(self):
        if not self.location:
            return None
        return self.location

#serverPermissionChoices = [(p.id,unicode(p)) for p in Permission.objects.filter(content_type__in=ContentType.objects.filter(app_label__in=appsettings.PERMISSION_CHOICES))]

class ServerPermission(models.Model):
    user = models.ForeignKey(User, related_name='server_permissions',verbose_name=_('Server Permissions'))
    server = models.ForeignKey(Server, related_name='user_permissions')
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True)
    permissions = models.ManyToManyField(Permission, verbose_name=_('User Permissions'), blank=True, limit_choices_to={'content_type__in': ContentType.objects.filter(app_label__in=appsettings.PERMISSION_CHOICES)})

    def __repr__(self):
        return "%s - %s" % (self.user.username, self.server.name)
    
    def __unicode__(self):
        return repr(self)
    
    class Meta:
        unique_together = ('user','server')

class AuditorManager(models.Manager):
    
    def get_by_client(self, clientId, server):
        return self.filter(clientid=clientId, server=server).order_by('-created')
    
    def get_by_client_n_user(self, clientId, server, user):
        return self.filter(clientid=clientId, server=server, user=user).order_by('-created')
    
class Auditor(models.Model):
    user = models.ForeignKey(User)
    server = models.ForeignKey(Server)
    clientid = models.IntegerField(db_index=True, default=0)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    message = models.CharField(max_length=765)
    
    objects = AuditorManager()
    
    def __repr__(self):
        return "%s - %s - %s - %s" % (self.user.username, self.server.name, self.created, self.message)
            
    def __unicode__(self):
        return repr(self)
            
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
#    canChangePassword = models.BooleanField(_('Can Change Password'), default=True,
#                                            help_text=_('Allow the user to change login password'))

    def __repr__(self):
        return self.user.username
    
    def __unicode__(self):
        return repr(self)

    class Meta:
        permissions = (
            ("change_password", "Change Login Password"),
        ) 

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
        
from b3portal import init_database_config

def update_db_callback(sender, **kwargs):
    init_database_config()

from django.db.models.signals import post_save
post_save.connect(update_db_callback, sender=Server)    