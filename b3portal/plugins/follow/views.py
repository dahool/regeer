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
from models import Follow
from common.view.decorators import render
from common.shortcuts import get_object_or_404
from b3connect.models import Client
from forms import FollowForm
import datetime
from django.utils.translation import gettext as _

from django.contrib import messages
from django.http import HttpResponseRedirect
from b3portal.plugins import is_plugin_enabled

from b3portal.permission.utils import server_permission_required_with_403
from b3portal import permissions as perm
from b3portal.resolver import urlreverse
from b3portal.models import Auditor
from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, InvalidPage

@server_permission_required_with_403(perm.FOLLOW_VIEW)
@render('follow/list.html')
def home(request):
    if not is_plugin_enabled(request.server, 'follow'):
        messages.info(request, _('This function is not enabled on this server.'))
        return {'client_list': None}  

    query = Follow.objects.using(request.server).all().order_by('-time_add')
    
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    paginator = Paginator(query, settings.ITEMS_PER_PAGE)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        lista = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lista = paginator.page(paginator.num_pages)
                
    return {'client_list': lista}

@server_permission_required_with_403(perm.FOLLOW_ADD)
@render('follow/add.html')
def add(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            p = Follow.objects.using(request.server).create(client=client,
                       reason=_("%(reason)s (by %(user)s)") % {'reason': form.cleaned_data['reason'], 'user': request.user},
                       time_add=datetime.datetime.now(),
                       admin_id=0)
            messages.success(request, _('Follow added successfully.'))
            
            Auditor.objects.create(user=request.user,
                                   server_id=request.server,
                                   clientid=client.id,
                                   message=_("Put %s") % str(p))
            
            return HttpResponseRedirect(urlreverse("client_detail",server=request.server,kwargs={'id':id}))
    else:
        if client.followed.all():
            messages.error(request, _('User already exists.'))
            return HttpResponseRedirect(urlreverse("client_detail",server=request.server,kwargs={'id':id}))            
        form = FollowForm()
        
    return {'form': form, 'client': client}

@server_permission_required_with_403(perm.FOLLOW_DELETE)
def remove(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    if client.followed.all():
        for r in client.followed.all():
            r.delete()

        Auditor.objects.create(user=request.user,
                               server_id=request.server,
                               clientid=client.id,
                               message=_("Remove from watch list"))
                    
        messages.success(request, _('User removed of the watch list'))    
    else:
        messages.error(request, _('User is not in the watch list'))

    if request.GET.has_key('ls'):
        return HttpResponseRedirect(urlreverse("follow:home",server=request.server))
    else:
        return HttpResponseRedirect(urlreverse("client_detail",server=request.server,kwargs={'id': id}))    
