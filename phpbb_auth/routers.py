# -*- coding: utf-8 -*-
"""Copyright (c) 2009 Sergio Gabriel Teves
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

PHPBB_DB = getattr(settings, 'PHPBB_DB_ID', 'phpbb')

class phpbbRouter(object):
    
    def _is_bb(self, model):
#            if model.__class__.__name__ in ('bbUser','bbGroup','bbAclRole','bbAclOption','bbUserGroup'): 
        if hasattr(model, '_meta'):       
            if model._meta.app_label == 'phpbb_auth':
                return True
        return False
    
    def db_for_read(self, model, **hints):
        if self._is_bb(model):
            return PHPBB_DB
        return None

    def db_for_write(self, model, **hints):
        if self._is_bb(model):
            return PHPBB_DB
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        return None
    
#    def allow_syncdb(self, db, model):
#        if self._is_bb(model):
#            return False
#        return None