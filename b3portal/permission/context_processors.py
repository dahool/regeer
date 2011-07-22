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
from django.utils.functional import lazy
from b3portal.permission.utils import has_server_perm

class PermLookupDict(object):
    def __init__(self, user, server, module_name):
        self.user, self.server, self.module_name = user, server, module_name

    def __repr__(self):
        return str(self.user.get_all_permissions())

    def __getitem__(self, perm_name):
        return has_server_perm(self.user,"%s.%s" % (self.module_name, perm_name), self.server)

    def __nonzero__(self):
        return self.user.has_module_perms(self.module_name)


class PermWrapper(object):
    def __init__(self, user, server):
        self.user = user
        self.server = server
        
    def __getitem__(self, module_name):
        return PermLookupDict(self.user, self.server, module_name)

    def __iter__(self):
        # I am large, I contain multitudes.
        raise TypeError("PermWrapper is not iterable.")

def perm(request):
    return {
        'obj_perms': lazy(lambda: PermWrapper(request.user, request.server), PermWrapper)(),
    }
