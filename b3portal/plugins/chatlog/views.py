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
import urllib
import time
import re

from common.view.decorators import render
from django.utils.translation import gettext as _
from django.contrib import messages
from models import ChatLog
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.conf import settings
from b3portal.plugins.chatlog.forms import ChatLogSearch
from django.db.models import Q
from b3portal.plugins import is_plugin_enabled

from b3portal.permission.utils import server_permission_required_with_403
from b3portal import permissions as perm

@server_permission_required_with_403(perm.CHATLOG_VIEW)
@render('chatlog/log.html')
#@flood
def chatlist(request):
    if not is_plugin_enabled(request.server, 'chatlog'):
        messages.info(request, _('This function is not enabled for this server.'))
        return {'chat_list': None}        
    
    chats = ChatLog.objects.using(request.server).all()

    # Make sure page request is an int. If not, deliver first page.   
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    search = None
    highlight = None
    if request.GET.has_key('search'):
        form = ChatLogSearch(request.GET)
        if form.is_valid():
            search = {}
            for k,v in request.GET.items():
                search[k]=v
            data = form.cleaned_data
            name = data['name']
            if len(name)>0:
                if re.search('^[@]{1}[0-9]*$',name):
                    chats = chats.filter(client__id=name[1:])
                elif re.search('^\+[@]{1}[0-9]*$',name):
                    highlight = int(name[2:]) 
                else:
                    chats = chats.filter(Q(client__name__icontains=name) | Q(client__aliases__alias__icontains=name)).distinct()
            datefrom = data['datefrom']
            if datefrom:
                chats = chats.filter(time_add__gte=time.mktime(datefrom.timetuple()))
            dateto = data['dateto']
            if dateto:
                chats = chats.filter(time_add__lte=time.mktime(dateto.timetuple()))
            text = data['text']
            if text:
                chats = chats.filter(data__icontains=text)
            map = data['map']
            if map:
                chats = chats.filter(info=map)
    else:
        form = ChatLogSearch()

    if search:
        search = urllib.urlencode(search)
            
    paginator = Paginator(chats, settings.ITEMS_PER_PAGE)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)

    return {'chat_list': list,
            'form': form,
            'search': search,
            'highlight': highlight}