# -*- coding: utf-8 -*-
"""Copyright (c) 2011-2012 Sergio Gabriel Teves
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
from b3portal.plugins import is_plugin_enabled
from django.http import Http404
from django.conf import settings

from b3portal.plugins.ctime.functions import get_player_activity

CACHE_TIMEOUT = getattr(settings, 'ACTIVITY_CACHE', 120) * 60

@server_permission_required_with_403(perm.VIEW_ACTIVITY)    
@cache_page(CACHE_TIMEOUT)
@render('activity/client_activity.html')
def client_detail(request, id):
    server = get_object_or_404(Server,uuid=request.server)

    if not is_plugin_enabled(server, 'ctime'):
        raise Http404
    
    client = get_object_or_404(Client, id=id, using=request.server)
    
    data = get_player_activity(client)

    return {'client': client, 'activity': data}