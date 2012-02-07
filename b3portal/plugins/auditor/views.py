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
from b3portal.permission.utils import server_permission_required_with_403
from b3portal import permissions as perm
from django.views.decorators.cache import cache_page
from common.view.decorators import render
from common.shortcuts import get_object_or_404
from b3connect.models import Client
from b3portal.client.views import _paginate
from b3portal.plugins.auditor.models import AuditLog

@server_permission_required_with_403(perm.VIEW_ADM_LOG)
@cache_page(15*60)
@render('b3portal/client/include/client_admin_logs.html')
def list_admin_actions(request, id):
    '''all actions an admin did on this user
    '''
    client = get_object_or_404(Client, id=id, using=request.server)
    notices = _paginate(request, client.admin_logs.all())
    return {'client_adm_logs': notices,
            'client': client}

@server_permission_required_with_403(perm.VIEW_USER_LOG)
@cache_page(15*60)
@render('b3portal/client/include/client_user_cmd.html')    
def list_commands(request, id):
    '''all actions performed by this user
    '''
    client = get_object_or_404(Client, id=id, using=request.server)
    notices = _paginate(request, client.commands.all())
    return {'client_adm_commands': notices,
            'client': client}
    
    