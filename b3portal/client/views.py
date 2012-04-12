# -*- coding: utf-8 -*-
"""Copyright (c) 2010-2012 Sergio Gabriel Teves
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

from common.shortcuts import get_object_or_404
from django.db.models import Q

from b3connect.models import Penalty, Client, Group, PENALTY_TYPE_NOTICE, TYPE_COMMENT
from b3portal.models import Server, Auditor, ServerBanList

from django.conf import settings

import time
import datetime

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.decorators.cache import cache_page
import urllib
from b3portal.client.forms import PenaltyForm, NoticeForm, CommentForm

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.translation import gettext as _
from common.utils.functions import time2minutes

from django.contrib import messages
from common.middleware.exceptions import Http403
from django.contrib.auth.decorators import login_required

#from common.floodprotection import flood
from common.query.functions import get_query_order

from django.core.cache import cache
from django.utils.datastructures import MultiValueDictKeyError

from b3portal.plugins import is_plugin_enabled, is_plugin_installed

from b3portal.permission.utils import server_permission_required_with_403, has_server_perm, has_any_server_perms
from b3portal import permissions as perm
from b3portal.resolver import urlreverse
from common.view.renders.json import get_json_value
from gameutils import load_banlist_all

from b3portal.client import signals

import logging
from django.template.loader import render_to_string

from django.utils.html import escape as escapehtml

logger = logging.getLogger(__name__)

@server_permission_required_with_403(perm.VIEW_CLIENT)
@render('b3portal/client/client.html')
def client(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    
    try:
        if client.group.level >= settings.HIGH_LEVEL_CLIENT:
            if not has_server_perm(request.user, perm.VIEW_HIGH_LEVEL_CLIENT, request.server):
                messages.warning(request, _('You are not authorized to view details about this player.'))
                raise Http403
    except Group.DoesNotExist:
        pass
    except Exception, e:
        logger.error(str(e))
        raise
    
    online = None
    server = Server.objects.get(uuid=request.server)
    if is_plugin_installed('status'):
        try:
            from b3portal.plugins.status.models import ServerStatus
            status = ServerStatus.objects.filter(server=server).latest()
            online = status.is_online(client.id)
        except:
            pass

    playedtime = None
    playedlastmonth = None
    if is_plugin_enabled(server, 'ctime'):
        try:
            from b3portal.plugins.ctime import functions as ctime
            from common.utils.timesince import minutes_to_string
            ptime = ctime.get_total_playtime(client)
            playedtime = {'start': ptime['since'], 'total': minutes_to_string(ptime['total'])}
            if (datetime.datetime.now() - ptime['since']).days > 30:
                ptime = ctime.get_total_playtime(client, datetime.datetime.now() - datetime.timedelta(days=30))
                playedlastmonth = {'start': ptime['since'], 'total': minutes_to_string(ptime['total'])}
        except:
            pass
            
    if has_server_perm(request.user, perm.VIEW_AUDITLOGS, request.server):
        client_auditlogs = _paginate(request, Auditor.objects.get_by_client(client.id, request.server)) 
    else:
        client_auditlogs = _paginate(request, Auditor.objects.get_by_client_n_user(client.id, request.server, request.user)) 
        #client_auditlogs = None
        
    client_aliases = _paginate(request, client.aliases.all())
    client_ipaliases = _paginate(request, client.ip_aliases.all())
    client_notices = _paginate(request, client.penalties.notices())
    client_penalties = _paginate(request, client.penalties.active_bans())
    client_ppenalties = _paginate(request, client.penalties.inactive())
    client_admactions = _paginate(request, client.adminpenalties.all())
    
    if is_plugin_enabled(server, "auditor"):
        client_actions = _paginate(request, client.commands.all())
        client_adm_actions = _paginate(request, client.admin_logs.all())
    else:
        client_actions = None
        client_adm_actions = None
        
    banlist = _get_banlist(request)
    
    groups = get_group_list(request, client)
    
    return {'client': client,
            'status': online,
            'banlist': banlist,
            'playedtime': playedtime,
            'playedlastmonth': playedlastmonth,
            'client_auditlogs': client_auditlogs,
            'client_aliases': client_aliases,
            'client_ipaliases': client_ipaliases,
            'client_notices': client_notices,
            'client_penalties': client_penalties,
            'client_ppenalties': client_ppenalties,
            'client_admactions': client_admactions,
            'client_adm_commands': client_actions,
            'client_adm_logs': client_adm_actions,            
            'group_data': get_json_value(groups),
            'change_group': len(groups) > 0}

def _get_banlist(request):
    if not has_server_perm(request.user, perm.VIEW_PENALTY, request.server):
        return []
    cache_key = "%s_banlist" % request.server
    lista = cache.get(cache_key)
    if lista is None:
        try:
            sb = ServerBanList.objects.get(server=request.server)
        except:
            return []
        if sb.get_file():
            lista = load_banlist_all(sb.get_file())
        else:
            return []
        cache.set(cache_key, lista, getattr(settings, 'BANLIST_CACHE_EXPIRE', 1440) * 60)
    return lista
        
@login_required
@cache_page(120*60)
@render('b3portal/client/world_map.html')
def player_map(request):
    from common.utils.geoip import GeoLocation
    countries = {}
    geo = GeoLocation()
    for client in Client.objects.using(request.server).filter(id__gt=1):
        country_name = geo.get_country(client.ip)
        if countries.has_key(country_name):
            count = countries.get(country_name) + 1
        else:
            count = 1
        countries[country_name]=count
    return {'list': countries}

@server_permission_required_with_403(perm.VIEW_HIGH_LEVEL_CLIENT)
@render('b3portal/client/admin_list.html')
def adminlist(request, filter=False):
    clients = Client.objects.using(request.server).filter(id__gt=1, group__level__gte=settings.HIGH_LEVEL_CLIENT)
    clients = clients.order_by('group__level')
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    res = {}
    if request.POST.has_key('days') or request.GET.has_key('days') or filter:
        days = request.POST.get('days') or request.GET.get('days') or 30
        dt = datetime.datetime.now() - datetime.timedelta(days=int(days))
        clients = clients.filter(time_edit__lte=time.mktime(dt.timetuple()))
        clients = clients.order_by('-time_edit')
        res['render_template'] = 'b3portal/client/inactiveadmin_list.html'
        res['days']=int(days)
        
    paginator = Paginator(clients, settings.ITEMS_PER_PAGE)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        lista = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lista = paginator.page(paginator.num_pages)
    
    res['client_list']=lista        
    return res

@server_permission_required_with_403(perm.VIEW_CLIENT)
@render('b3portal/client/client_list.html')
@cache_page(30)
def clientlist(request):
    data = ''
    search = {'server': request.server}
    filter = 'name'
    
    if request.GET.has_key('sort'):
        sort = request.GET.get('sort')
        order = request.GET.get('order') or 'asc'
        search['sort'] = sort
        search['order'] = order
            
#    if request.GET.has_key('searchall') and request.user.has_perm(perm.PERFORM_ADV_SEARCH):
#        field = request.GET['type']
#        data = request.GET['data']
#        list = {}
#        for server in request.server_list:
#            list[server.uuid] = _getclientlist(request, server.uuid)
#        return {'list': list, 'field': field, 'data': data, 'search': urllib.urlencode(search)}
#    elif
    if request.GET.has_key('search') or request.GET.has_key('searchall'):
        for k,v in request.GET.items():
            # there is an odd bug I can't identify
            # sometimes type is passed as ?type
            if k == '?type':
                k = 'type'
            search[k]=v
        data = search['data']
        filter = search['type']
        clients = _getclientlist(request, request.server)
    else:
        clients = _getclientlist(request, request.server, False)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    paginator = Paginator(clients, settings.ITEMS_PER_PAGE)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        lista = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lista = paginator.page(paginator.num_pages)
    
    return {'client_list': lista, 'filter': filter, 'data': data, 'search': urllib.urlencode(search), 'order_by': get_query_order(clients)}

def _getclientlist(request, server, search = True):

    if has_server_perm(request.user, perm.VIEW_HIGH_LEVEL_CLIENT, server):
        clients = Client.objects.using(server).filter(id__gt=1)
    else:
        clients = Client.objects.using(server).filter(Q(group__level__lt=settings.HIGH_LEVEL_CLIENT) | Q(group__isnull=True), id__gt=1)
    
    if search:
        try:
            field = request.GET['type']
        except MultiValueDictKeyError, e:
            logger.warning(str(e))
            field = request.GET['?type']
        data = request.GET['data']
        filter = field
        if field == 'name':
            clients = clients.filter(Q(name__icontains=data) | Q(aliases__alias__icontains=data)).distinct()
        elif field == 'id':
            try:
                clients = clients.filter(id=int(data))
            except:
                clients =[]
        elif field == 'ip':
            if settings.SUPPORT_IP_ALIASES:
                clients = clients.filter(Q(ip__startswith=data) | Q(ip_aliases__ip__startswith=data)).distinct()
            else:
                clients = clients.filter(ip__startswith=data).distinct()
    
    if request.GET.has_key('sort'):
        sort = request.GET.get('sort')
        order = request.GET.get('order') or 'asc'
        if order == 'desc':
            sort = "-%s" % sort
        clients = clients.order_by(sort)
        
    if request.GET.has_key('level'):
        if not has_server_perm(request.user, perm.VIEW_GROUP, server):
            raise Http403
        if request.GET.get('level'):
            clients = clients.filter(group__level=request.GET.get('level'))
        else:
            clients = clients.filter(group__isnull=True)            
    
    return clients

@server_permission_required_with_403(perm.VIEW_CLIENT)
@cache_page(30*60)
@render('b3portal/client/regular_client_list.html')
def regularclients(request):
    dt = datetime.datetime.now() - datetime.timedelta(days=7)
    clients = Client.objects.using(request.server).filter(id__gt=1, connections__gte=50, time_edit__gte=time.mktime(dt.timetuple()))
    clients = clients.order_by('-time_edit')

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    paginator = Paginator(clients, settings.ITEMS_PER_PAGE)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        lista = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lista = paginator.page(paginator.num_pages)
        
    return {'client_list': lista}

@login_required
@render('b3portal/client/add_penalty.html')
def addpenalty(request, id, notice=False):
    
    if notice:
        if not has_any_server_perms(request.user, [perm.ADD_NOTICE, perm.ADD_PENALTY], request.server):
            raise Http403
    else:
        if not has_server_perm(request.user, perm.ADD_PENALTY, request.server):
            raise Http403
            
    client = get_object_or_404(Client, id=id, using=request.server)
    if notice:
        frmObj = NoticeForm
    else:
        frmObj = PenaltyForm
    if request.method == 'POST':
        form = frmObj(request.POST)
        if form.is_valid():
            p = Penalty(client=client,
                        reason= form.cleaned_data['reason'],
                        time_edit=datetime.datetime.now(),
                        time_add=datetime.datetime.now(),
                        data= "UP#%s" % request.user.username,
                        admin_id=0)
            if form.Meta.type == 1:
                p.duration=0
                p.type='Notice'
            else:
                if form.cleaned_data['permanent']:
                    p.duration=0
                    p.type='Ban'
                else:
                    #dt = time2minutes(str(form.cleaned_data['time'])+form.cleaned_data['time_type'])
                    p.duration = form.cleaned_data['time']
                    p.type='TempBan'
            p.save(using=request.server)
            Auditor.objects.create(user=request.user,
                                   server_id=request.server,
                                   clientid=client.id,
                                   message=_("Add \"%s\"") % str(p))
            try:
                signals.add_penalty.send(sender=p, user=request.user,
                                                client=client,
                                                penalty=p,
                                                server=request.server)
            except Exception, e:
                logger.error(str(e))
            if notice:
                messages.success(request, _('Notice added successfully.'))
            else:
                messages.success(request, _('Penalty added successfully.'))
            return HttpResponse("{\"sucess\": true}", mimetype='application/json') 
            #return HttpResponseRedirect(urlreverse("client_detail", server=request.server, kwargs={'id':id}))
    else:
        form = frmObj()
    if notice:
        url = urlreverse("add_notice", server=request.server, kwargs={'id':id})
    else:
        url = urlreverse("add_penalty", server=request.server, kwargs={'id':id})
    return {'form': form, 'client': client, 'url': url}

@server_permission_required_with_403(perm.ADD_NOTES)
@render('b3portal/client/add_note.html')
def addnote(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # penalty type in db is defined as enum.
            # so we treat a comment like an inactive notice with a special keyword
            p = Penalty(client=client,
                        type=PENALTY_TYPE_NOTICE,
                        keyword=TYPE_COMMENT,
                        inactive=1,
                        duration=0,
                        reason= form.cleaned_data['reason'],
                        time_edit=datetime.datetime.now(),
                        time_add=datetime.datetime.now(),
                        data= "UP#%s" % request.user.username,
                        admin_id=0)
            p.save(using=request.server)
            Auditor.objects.create(user=request.user,
                                   server_id=request.server,
                                   clientid=client.id,
                                   message=_("Add \"%s\"") % str(p))
            messages.success(request, _('Comment added successfully.'))
            return HttpResponse("{\"sucess\": true}",  mimetype='application/json') 
    else:
        form = CommentForm()
        url = urlreverse("add_note", server=request.server, kwargs={'id':id})
    return {'form': form, 'client': client, 'url': url}

@server_permission_required_with_403(perm.DELETE_NOTES)
@render('b3portal/client/add_note.html')
def removenote(request, id):
    penalty = get_object_or_404(Penalty, id=id, using=request.server)
    Auditor.objects.create(user=request.user,
                           server_id=request.server,
                           clientid=penalty.client.id,
                           message=_("Remove \"%s\"") % str(penalty))
    penalty.delete()        
    messages.success(request, _('Comment removed successfully.'))
    return HttpResponse("{\"sucess\": true}", mimetype='application/json')

@login_required
def removenotice(request, id):
    
    if not has_any_server_perms(request.user, [perm.DELETE_NOTICE, perm.DELETE_PENALTY], request.server):
        raise Http403
    
    penalty = get_object_or_404(Penalty, id=id, using=request.server)
    if (penalty.type != PENALTY_TYPE_NOTICE):
        raise Http403
    Auditor.objects.create(user=request.user,
                           server_id=request.server,
                           clientid=penalty.client.id,
                           message=_("Remove \"%s\"") % str(penalty))
    try:
        signals.delete_penalty.send(sender=penalty, user=request.user,
                                        client=penalty.client,
                                        penalty=penalty,
                                        server=request.server)        
    except Exception, e:
        logger.error(str(e))
    penalty.delete()        
    messages.success(request, _('Notice removed successfully.'))
    return HttpResponse("{\"sucess\": true}", mimetype='application/json')
    #return HttpResponseRedirect(urlreverse("client_detail",server=request.server, kwargs={'id':penalty.client.id}))
    
@server_permission_required_with_403(perm.DELETE_PENALTY)
def disablepenalty(request, id):
    penalty = get_object_or_404(Penalty, id=id, using=request.server)
    penalty.inactive = 1
    penalty.save()
    Auditor.objects.create(user=request.user,
                           server_id=request.server,
                           clientid=penalty.client.id,
                           message=_("Disable \"%s\"") % str(penalty))
    try:
        signals.delete_penalty.send(sender=penalty,
                                        user=request.user,
                                        client=penalty.client,
                                        penalty=penalty,
                                        server=request.server)
    except Exception, e:
        logger.error(str(e))
        
    messages.success(request, _('Penalty de-activated successfully.'))
    return HttpResponse("{\"sucess\": true}", mimetype='application/json')
    #return HttpResponseRedirect(urlreverse("client_detail",server=request.server, kwargs={'id':penalty.client.id}))

@server_permission_required_with_403(perm.CHANGE_PENALTY)
@render('b3portal/client/add_penalty.html')
def editpenalty(request, id):
    p = get_object_or_404(Penalty, id=id, using=request.server)
    if request.method == 'POST':
        form = PenaltyForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['permanent']:
                p.duration=0
                p.type='Ban'
            else:
                p.duration = form.cleaned_data['time']
                p.type='TempBan'
            p.reason = form.cleaned_data['reason']
            p.time_edit=datetime.datetime.now()
            p.save()
            Auditor.objects.create(user=request.user,
                                   server_id=request.server,
                                   clientid=p.client.id,
                                   message=_("Update \"%s\"") % str(p))            
            messages.success(request, _('Penalty updated.'))
            try:
                signals.change_penalty.send(sender=p,
                                            user=request.user,
                                                client= p.client,
                                                penalty=p,
                                                server=request.server)
            except Exception, e:
                logger.error(str(e))
            #return HttpResponseRedirect(urlreverse("client_detail",server=request.server,kwargs={'id':p.client.id}))
            return HttpResponse("{\"sucess\": true}", mimetype='application/json')
    else:
        if p.duration==0:
            form = PenaltyForm(initial={'permanent': True, 'reason': p.reason})
        else:
            form = PenaltyForm(initial={'permanent': False, 'reason': p.reason,
                                        'time': p.duration,
                                        'time_type': 'm'})
    url = urlreverse("edit_penalty", server=request.server, kwargs={'id':id})            
    return {'form': form, 'client': p.client, 'url': url}

@login_required
def change_clientgroup(request, id):
    
    if request.method != 'POST':
        raise Http403

    g = int(request.POST.get('value'))
    if not has_server_perm(request.user, perm.CLIENT_GROUP_CHANGE, request.server):
        if g < 2 and has_any_server_perms(request.user, [perm.CLIENT_REGISTER, perm.CLIENT_REGULAR, perm.CLIENT_REMOVE_REGULAR, perm.CLIENT_REMOVE_REGISTER], request.server):
            pass
        elif g == 2 and has_server_perm(request.user, perm.CLIENT_REGULAR, request.server):
            pass
        else:
            raise Http403        
     
    group = get_object_or_404(Group, id=g, using=request.server)
    client = get_object_or_404(Client, id=id, using=request.server)

    try:
        currentLevel = client.group.level if client.group else 0
    except Group.DoesNotExist:
        currentLevel = 0
        
    if g == 100 or currentLevel == 100:
        server = get_object_or_404(Server, pk=request.server)
        if not (request.user.is_superuser or server.is_owner(request.user)):
            raise Http403
        
    if client.group_id > group.id:
        if client.group_id == 2 and has_server_perm(request.user, perm.CLIENT_REMOVE_REGULAR, request.server):
            pass
        elif client.group_id == 1 and has_server_perm(request.user, perm.CLIENT_REMOVE_REGISTER, request.server):
            pass
        elif has_server_perm(request.user, perm.CLIENT_GROUP_CHANGE, request.server):
            pass
        else:
            messages.error(request, _('You are not authorized to update this client at this time.'))
            return HttpResponse(str(client.group), mimetype='plain/text')
        upgrade = False
    else:
        upgrade = True
    
    client.group = group
    client.save()

    if upgrade:
        Auditor.objects.create(user=request.user,
                           server_id=request.server,
                           clientid=client.id,
                           message=_("Upgrade client to \"%s\"") % group.name)
    else:
        Auditor.objects.create(user=request.user,
                           server_id=request.server,
                           clientid=client.id,
                           message=_("Downgrade client to \"%s\"") % group.name)

    try:
        signals.update_player_group.send(sender=client, user=request.user,
                                        client=client,
                                        server=request.server)
    except Exception, e:
        logger.error(str(e))
    
    messages.info(request, _('Client updated.'))
    return HttpResponse(str(group), mimetype='plain/text')

@server_permission_required_with_403(perm.VIEW_NOTES)
@render('b3portal/client/include/client_noteline.html')
def more_notes(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    p = client.penalties.comments()[:1][0]
    return {'note': p}

@server_permission_required_with_403(perm.VIEW_ALIAS)
@cache_page(15*60)
@render('b3portal/client/include/client_aliases.html')
def more_alias(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    client_aliases = _paginate(request, client.aliases.all())
    return {'client_aliases': client_aliases, 'client': client}

@server_permission_required_with_403(perm.VIEW_ALIAS)
@cache_page(15*60)
@render('b3portal/client/include/client_ipaliases.html')
def more_ipalias(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    ipaliases = _paginate(request, client.ip_aliases.all())
    return {'client_ipaliases': ipaliases,
            'banlist': _get_banlist(request),
            'client': client}

@server_permission_required_with_403(perm.VIEW_HIGH_LEVEL_CLIENT)
@cache_page(15*60)
@render('b3portal/client/include/client_adminactions.html')
def more_admactions(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    client_admactions = _paginate(request, client.adminpenalties.all())
    return {'client_admactions': client_admactions,
            'client': client}

@server_permission_required_with_403(perm.VIEW_PENALTY)
@render('b3portal/client/include/client_penalties.html')
def more_penalties(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    client_penalties = _paginate(request, client.penalties.active_bans())
    return {'client_penalties': client_penalties,
            'client': client }
    
@server_permission_required_with_403(perm.VIEW_PENALTY)
@render('b3portal/client/include/client_ipenalties.html')
def more_ipenalties(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    client_ppenalties = _paginate(request, client.penalties.inactive())
    return {'client_ppenalties': client_ppenalties,
            'client': client }

@server_permission_required_with_403(perm.VIEW_PENALTY)
@render('b3portal/client/include/client_notices.html')
def more_notices(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    notices = _paginate(request, client.penalties.notices())
    return {'client_notices': notices,
            'client': client}

@render('b3portal/client/include/client_audit.html')
def more_logs(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    if has_server_perm(request.user, perm.VIEW_AUDITLOGS, request.server):
        client_auditlogs = _paginate(request, Auditor.objects.get_by_client(client.id, request.server)) 
    else:
        client_auditlogs = _paginate(request, Auditor.objects.get_by_client_n_user(client.id, request.server, request.user))
    #client_auditlogs = _paginate(request, Auditor.objects.get_by_client(client.id, request.server))
    return {'client_auditlogs': client_auditlogs,
            'client': client}

def direct(request):
    if request.method != 'POST':
        raise Http403
    pid = request.POST.get('playerid')
    next = request.POST.get('next')
    server = request.POST.get('server')
    
    if not has_server_perm(request.user, perm.VIEW_CLIENT, server):
        messages.error(request, _('You don\'t have enough permissions to search on that server.'))
        return HttpResponseRedirect(next)
    
    try:
        pid = int(pid)
    except:
        messages.error(request, _('You entered an invalid player id.'))
        return HttpResponseRedirect(next)
    try:
        player = Client.objects.using(server).get(id=pid)
    except Client.DoesNotExist:
        messages.warning(request, _('A player with id %d was not found.' % pid))
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(urlreverse("client_detail",server=request.server,kwargs={'id':player.id}))

@render('json')
@cache_page(5*60)
def group_list(request, id):
    client = get_object_or_404(Client, id=id, using=request.server);
    return get_group_list(request, client) 

def get_group_list(request, client):
    dict = {}
    query = Group.objects.using(request.server)
    groups= []
    if has_server_perm(request.user, perm.CLIENT_GROUP_CHANGE, request.server):
        server = Server.objects.get(pk=request.server)
        if (request.user.is_superuser or server.is_owner(request.user)):
            groups = query.all()
        else:
            groups = query.all().exclude(level=100)
    elif client.group_id == 2 and has_server_perm(request.user, perm.CLIENT_REMOVE_REGULAR, request.server):
        if has_server_perm(request.user, perm.CLIENT_REMOVE_REGISTER, request.server):
            groups = query.filter(level__lte=2)
        else:
            groups = query.filter(level__lte=2).exclude(level=0)
    elif client.group_id < 2:
        if has_server_perm(request.user, perm.CLIENT_REGULAR, request.server):
            if has_server_perm(request.user, perm.CLIENT_REMOVE_REGISTER, request.server):
                groups = query.filter(level__lte=2)
            else:
                groups = query.filter(level__lte=2).exclude(level=0)
        elif client.group_id == 1 and has_server_perm(request.user, perm.CLIENT_REMOVE_REGISTER, request.server):
            groups = query.filter(level__lte=1)
        elif client.group_id == 0 and has_server_perm(request.user, perm.CLIENT_REGISTER, request.server):
            groups = query.filter(level__lte=1).exclude(level=0) 
    
    for group in groups:
        dict[group.id]=str(group)
 
    return dict     

def _paginate(request, data):
    paginator = Paginator(data, settings.ITEMS_ON_CLIENT_PAGE)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
            
    try:
        lista = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lista = paginator.page(paginator.num_pages)
    
    return lista
    