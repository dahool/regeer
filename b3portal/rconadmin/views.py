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
from common.view.decorators import render

from django.shortcuts import render_to_response
from common.shortcuts import get_object_or_404
from django.template.context import RequestContext
from django.db.models import Q

from b3portal.plugins.map.models import Map
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from common.decorators import superuser_required

import time
from common.middleware.exceptions import Http403
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from django.core import validators
from django.utils.encoding import smart_unicode

from gameutils import load_banlist
from b3portal.models import Server
from b3portal.rconadmin.handlers.iourt41 import Iourt41RconHandler
from django.contrib.auth.decorators import login_required
from b3portal.permission.utils import has_server_perm
import b3portal.permissions as perm

@login_required
@render('b3portal/admin/home.html')
def home(request):
    if not has_server_perm(request.user, perm.RCON, request.server):
        raise Http403
    server = get_object_or_404(Server, uuid=request.server)
    if not server.support_rcon:
        messages.info(request, _('Server %s does not have RCON support enabled.' % server.name))
    # TODO load handler based on server
    h = Iourt41RconHandler(server=server)
    return {'form': h.form} 

@login_required    
@render('json')
def execute(request):
    if not has_server_perm(request.user, perm.RCON, request.server):
        raise Http403
    if request.method != 'POST':
        raise Http403
    server = get_object_or_404(Server, uuid=request.server)
    handler = Iourt41RconHandler(server=server, data=request.POST)
    resp = handler.execute()
    return {'success': False, 'response': '<br/>'.join(resp)}