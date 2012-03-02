# -*- coding: utf-8 -*-
"""Copyright (c) 2011,2012 Sergio Gabriel Teves
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
from b3portal.plugins.map.models import Map
from django.views.decorators.cache import cache_page
from b3portal.permission.utils import has_server_perm
from b3portal import permissions as perm
from django.contrib.auth.decorators import login_required
from common.shortcuts import get_object_or_404
from b3portal.models import Server

@cache_page(60*60)
@render('map/map_list.html')
def maps(request):
    maps = Map.objects.all()
    return {'maps': maps}

@login_required
@render('map/map_editor.html')
def map_editor(request, id):
    server = get_object_or_404(Server, pk=id)
    if not has_server_perm(request.user, perm.MAP_EDIT, id):
        pass
    maps = Map.objects.filter(server=server)
    return {'maps': maps, 'server': server}