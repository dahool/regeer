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
from common.view.decorators import render

from django.db.models import Q

from b3connect.models import Penalty
from django.conf import settings

import time
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from django.views.decorators.cache import cache_page

import urllib
from django.contrib.auth.decorators import login_required

from b3portal.permission.utils import server_permission_required_with_403, has_any_server_perms
from b3portal import permissions as perm
from common.middleware.exceptions import Http403

#from common.floodprotection import flood

@cache_page(60*60)
@render('b3portal/penalties/ban_list.html')
#@flood
def banlist(request):
    penalties = Penalty.objects.using(request.server).filter(Q(type='ban') | Q(type='tempban'),
                           Q(time_expire='-1') | Q(time_expire__gt=int(time.time())),
                           inactive=0)

    search = None
    if request.GET.has_key('search'):
        search = {}
        for k,v in request.GET.items():
            search[k]=v
        name = request.GET['name']
        penalties = penalties.filter(Q(client__name__icontains=name) | Q(client__aliases__alias__icontains=name)).distinct()

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    paginator = Paginator(penalties, settings.ITEMS_PER_PAGE)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)

    if search:
        search['server']=request.server
        search = urllib.urlencode(search)
        
    return {'ban_list': list, 'search': search}
    
@login_required
@cache_page(120*60)
@render('b3portal/penalties/world_map_banned.html')
#@flood
def banned_player_map(request):
    from common.utils.geoip import GeoLocation
    countries = {}
    geo = GeoLocation()
    for penalty in Penalty.objects.db_manager(request.server).active():
        country_name = geo.get_country(penalty.client.ip)
        if countries.has_key(country_name):
            count = countries.get(country_name) + 1
        else:
            count = 1
        countries[country_name]=count
    return {'list': countries}

@server_permission_required_with_403(perm.VIEW_PENALTY)
@cache_page(30*60)
@render('b3portal/penalties/kick_list.html')
def kicklist(request):
    penalties = Penalty.objects.using(request.server).filter(type='kick',admin__id__gt=0)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    paginator = Paginator(penalties, settings.ITEMS_PER_PAGE)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)

    return {'ban_list': list}

@server_permission_required_with_403(perm.VIEW_PENALTY)
@cache_page(30*60)
@render('b3portal/penalties/penalty_list.html')
def penalty_list(request):
    penalties = Penalty.objects.using(request.server).filter(Q(type='kick') | Q(type='warning'))

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    paginator = Paginator(penalties, settings.ITEMS_PER_PAGE)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)

    return {'ban_list': list}

@cache_page(30*60)
@render('b3portal/penalties/notice_list.html')
def notice_list(request):
    if not has_any_server_perms(request.user, [perm.VIEW_NOTICE, perm.VIEW_PENALTY], request.server):
        raise Http403
    
    penalties = Penalty.objects.using(request.server).filter(Q(type='Notice'))

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    paginator = Paginator(penalties, settings.ITEMS_PER_PAGE)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)

    return {'ban_list': list}