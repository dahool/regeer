# -*- coding: utf-8 -*-
"""Copyright (c) 2009, Sergio Gabriel Teves
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
from django.conf import settings
from datetime import datetime
from django.utils.encoding import force_unicode

from django.contrib.auth.models import Group

from phpbb_auth.settings import GROUP_MAPPING
from phpbb_auth.password import PhpbbPassword


PHPBB_TABLES_PREFIX = getattr(settings, 'PHPBB_TABLES_PREFIX','phpbb_')

class bbUser(models.Model):
    """Model for phpBB user."""
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    username_clean = models.CharField(max_length=255)
    user_password = models.CharField(max_length=40)
    user_email = models.CharField(max_length=255)
    user_regdate_int = models.IntegerField(db_column="user_regdate")
    user_lastvisit_int = models.IntegerField(db_column="user_lastvisit")
    
    def __repr__(self):
        return self.username
    
    def __unicode__(self):
        return repr(self)
    
    @property
    def user_regdate(self):
        return datetime.fromtimestamp(self.user_regdate_int)
    
    @property
    def user_lastvisit(self):
        return datetime.fromtimestamp(self.user_lastvisit_int)

    def check_password(self, password):
        phpbb_checker = PhpbbPassword()
        return phpbb_checker.phpbb_check_hash(password, self.user_password)
                    
    class Meta:
        db_table = PHPBB_TABLES_PREFIX + 'users'
        ordering = ['username_clean']

class bbGroup(models.Model):
    group_id = models.IntegerField(primary_key=True)
    group_type = models.IntegerField()
    group_founder_manage = models.IntegerField()
    group_name = models.CharField(max_length=255)
    group_desc = models.TextField()
    group_desc_bitfield = models.CharField(max_length=255)
    group_desc_options = models.IntegerField()

    def __repr__(self):
        return self.group_name
    
    def __unicode__(self):
        return repr(self)
    
    @property
    def local_group(self):
        try:
            return Group.objects.get(name=GROUP_MAPPING.get(self.group_name))
        except:
            return None
        
    class Meta:
        db_table = PHPBB_TABLES_PREFIX + 'groups'
        ordering = ['group_id']

class bbUserGroup(models.Model):
    group = models.ForeignKey(bbGroup, to_field="group_id", db_column="group_id", related_name='users', primary_key=True)
    user = models.ForeignKey(bbUser, to_field="user_id", db_column="user_id", related_name='groups')
    
    class Meta:
        db_table = PHPBB_TABLES_PREFIX + 'user_group'
            
class bbAclRole(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=255)
    role_description = models.TextField()
    role_type = models.CharField(max_length=10)
    role_order = models.IntegerField()

    def __repr__(self):
        self.role_name
        
    def __unicode__(self):
        return force_unicode(repr(self))
    
    class Meta:
        db_table = PHPBB_TABLES_PREFIX + 'acl_roles'
        ordering = ['role_name']

class bbAclOption(models.Model):
    auth_option_id = models.IntegerField(primary_key=True)
    auth_option = models.CharField(max_length=60)
    is_global = models.IntegerField()
    is_local = models.IntegerField()
    founder_only = models.IntegerField()
    
    def __repr__(self):
        self.auth_option
        
    def __unicode__(self):
        return force_unicode(repr(self))
        
    class Meta:
        db_table = PHPBB_TABLES_PREFIX + 'acl_options'
        ordering = ['auth_option_id']
        
class bbSession(models.Model):
    session_id = models.CharField(max_length=32, primary_key=True)
    session_user_id = models.IntegerField()
    session_ip = models.CharField(max_length=40)
    session_start = models.IntegerField()
    
    class Meta:
        db_table = PHPBB_TABLES_PREFIX + 'sessions'
            
class bbSessionKey(models.Model):
    key_id = models.CharField(max_length=32, primary_key=True)
    user_id = models.IntegerField()
    last_ip = models.CharField(max_length=40)
    last_login = models.IntegerField()
    
    class Meta:
        db_table = PHPBB_TABLES_PREFIX + 'sessions_keys'
    