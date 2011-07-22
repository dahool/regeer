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
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission

class ServerPermissionBackend(ModelBackend):
    
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False
    
    def get_group_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        if obj is None: return False
        if not hasattr(user_obj, '_server_%s_group_perm_cache' % obj.pk):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = []
                serverPerms = user_obj.server_permissions.filter(server=obj)
                for serverPerm in serverPerms:
                    for group in serverPerm.groups.all():
                        perms.extend(group.permissions.values_list('content_type__app_label', 'codename').order_by())
            setattr(user_obj, '_server_%s_group_perm_cache' % obj.pk, set(["%s.%s" % (ct, name) for ct, name in perms]))
        return getattr(user_obj, '_server_%s_group_perm_cache' % obj.pk)

    def get_all_permissions(self, user_obj, obj=None):
        if obj is None: return False
        if not hasattr(user_obj, '_server_%s_perm_cache' % obj.pk):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = set()
                serverPerms = user_obj.server_permissions.filter(server=obj)
                for serverPerm in serverPerms:
                    perms.update(set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in serverPerm.permissions.select_related()]))
                perms.update(self.get_group_permissions(user_obj, obj))
            setattr(user_obj, '_server_%s_perm_cache' % obj.pk, perms)
        return getattr(user_obj, '_server_%s_perm_cache' % obj.pk)

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None: return False
        return perm in self.get_all_permissions(user_obj, obj)
