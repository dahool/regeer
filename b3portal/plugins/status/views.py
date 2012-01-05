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
from common.view.decorators import render
from django.views.decorators.cache import cache_page
from b3portal.plugins.status.models import ServerStatus, StatusPlugin
from django.contrib import messages
from django.utils.translation import gettext as _

import datetime
from common.collections import OrderedDict
from common.utils.dateutil import datetimeIterator
from common.shortcuts import get_object_or_404

from b3connect.models import Client
from b3portal.models import Server

from b3portal.permission.utils import server_permission_required_with_403
from b3portal import permissions as perm

@server_permission_required_with_403(perm.STATUS_VIEWSTATUS)    
@cache_page(60)
@render('status/game_status.html')
def game_status(request):
    try:
        plugin = StatusPlugin.objects.get(server=get_object_or_404(Server,uuid=request.server))
    except StatusPlugin.DoesNotExist:
        return {}
    try:
        status = plugin.get_status()
    except Exception, e:
        messages.error(request, _('Error: %s' % str(e)))
        return {}
    return {"status": status}

@server_permission_required_with_403(perm.STATUS_VIEWSTATUS)    
@cache_page(60*60)
@render('status/client_detail.html')
def client_detail(request, id):
    server = Server.objects.get(uuid=request.server)
    status = ServerStatus.objects.filter(server=server,
                                       players__client_id=id)
    client = get_object_or_404(Client, id=id, using=request.server)
    return {"client": client,"status": status}

@server_permission_required_with_403(perm.STATUS_VIEWSTATUS)    
@cache_page(60*60)
@render('status/players_chart.html')
def player_chart(request):
    format = '%I%p'
    data = OrderedDict()
    # initialize the dict
    to_date = datetime.datetime.now()
    from_date = datetime.datetime.now()+datetime.timedelta(hours=-23)
    to_date = to_date.replace(minute=59, second=59)
    from_date = from_date.replace(minute=0, second=0)
    for n in datetimeIterator(from_date, to_date, datetime.timedelta(hours=1)):
        key = n.strftime(format).lower()
        data[key]=0
    server = Server.objects.get(uuid=request.server)
    list = ServerStatus.objects.filter(server=server,
                                       time_add__gte=from_date,
                                       time_add__lte=to_date) 
    for s in list:
        key = s.time_add.strftime(format).lower()
        if s.totalPlayers > data[key]: 
            data[key] = s.totalPlayers
    return {'list': data}