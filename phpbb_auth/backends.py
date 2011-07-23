# -*- coding: UTF-8 -*-
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

from django.contrib.auth.models import User, Permission
from django.contrib.auth.backends import ModelBackend
from models import bbUser

class phpbbBackend(ModelBackend):
    """
    Authenticates against phpbb database.
    Create local django user if success.
    """
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
    
    def authenticate(self, username=None, password=None):
        try:
            user = bbUser.objects.get(username_clean=username.lower())
        except bbUser.DoesNotExist:
            return None

        if user.check_password(password):
            try:
                localuser = User.objects.get(username=username)
            except User.DoesNotExist:
                localuser = User.objects.create(username=username,
                                                email=user.user_email)
                localuser.set_unusable_password()
                localuser.save()
            # localuser.set_password(password)
            # cache the phpbb user
            localuser._phpbb_user_cache = user
            localuser.is_phpbb = True
            return localuser
        
        return None
    
    def get_group_permissions(self, user_obj):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        if not hasattr(user_obj, '_group_perm_cache'):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                # get local user groups
                local_perms = Permission.objects.filter(group__user=user_obj).values_list('content_type__app_label', 'codename').order_by()
                perms = set(["%s.%s" % (ct, name) for ct, name in local_perms])
                # get user groups from phpbb groups
                try:
                    if not hasattr(user_obj, '_phpbb_user_cache'):
                        bbuser = bbUser.objects.get(username=user_obj.username)
                        user_obj._phpbb_user_cache = bbuser
                    else:
                        bbuser = user_obj._phpbb_user_cache
                except bbUser.DoesNotExist:
                    # something is wrong.
                    pass
                else:
                    for groupRel in bbuser.groups.all():
                        group = groupRel.group.local_group
                        if group:
                            bb_perms = Permission.objects.filter(group=group).values_list('content_type__app_label', 'codename').order_by()
                            perms.update(["%s.%s" % (ct, name) for ct, name in bb_perms])
            user_obj._group_perm_cache = perms
        return user_obj._group_perm_cache