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
from django.conf import settings
from django.contrib.auth.models import Group, Permission

class AnonymousSupportBackend:
    supports_object_permissions = False
    supports_anonymous_user = True
    supports_inactive_user = False    
    
    def authenticate(self, username=None, password=None):
        return None
    
    def has_perm(self, user_obj, perm):
        if user_obj.is_anonymous():
            if not hasattr(user_obj, '_guest_perm_cache'):
                try:
                    g = Group.objects.get(name=getattr(settings, "ANONYMOUS_GROUP", "Guest"))
                except Group.DoesNotExist:
                    user_obj._guest_perm_cache = []
                    return False
                else:
                    perms = [u"%s.%s" % (ct, name) for ct, name in Permission.objects.filter(group=g).values_list('content_type__app_label', 'codename').order_by()]
                    user_obj._guest_perm_cache = perms
            else:
                perms = user_obj._guest_perm_cache
            return perm in perms
        return False