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
from b3portal.models import Server
from b3portal.plugins import PLUGINS
from common.middleware.exceptions import Http403
from common.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger('regeer')

@login_required
@render("b3portal/server/index.html")
def index(request):
    if request.user.is_superuser:
        servers = Server.objects.all()
    else:
        servers = request.user.owned_servers.all()

    if not servers:
        raise Http403
        
    return {'server': servers[0],
            'servers': servers,
            'plugins': PLUGINS}
    
@login_required
@render("b3portal/server/server_tab.html")    
def get_server(request, id):
    server = get_object_or_404(Server, pk=id)
    if not request.user.is_superuser and not server.is_owner(request.user):
        raise Http403
    
    return {'server': server,
            'plugins': PLUGINS}