from common.view.decorators import render

from common.shortcuts import get_object_or_404
from django.db.models import Q

from b3connect.models import Penalty, Client, Group
from django.conf import settings

import time
import datetime

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from common.decorators import permission_required_with_403
from django.views.decorators.cache import cache_page
import urllib
from b3portal.client.forms import PenaltyForm, NoticeForm

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import gettext as _
from common.utils.functions import time2minutes

from django.contrib import messages
from common.middleware.exceptions import Http403
from django.contrib.auth.decorators import login_required

from common.floodprotection import flood
from common.query.functions import get_query_order

from django.core.cache import cache
from gameutils import load_banlist
from common.utils.application import is_plugin_installed
from django.utils.datastructures import MultiValueDictKeyError

@permission_required_with_403('b3connect.view_client')
@cache_page(15*60)
@render('b3portal/client/client.html')
def client(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    
    try:
        if client.group.level >= settings.HIGH_LEVEL_CLIENT:
            if not request.user.has_perm('b3connect.view_high_level_client'):
                messages.warning(request, _('You are not authorized to view details about this player.'))
                raise Http403
    except Group.DoesNotExist:
        pass
    except:
        raise
    
    online = None
    if is_plugin_installed('status'):
        from plugins.status import get_server_status
        status = get_server_status(request.server)
        if status.clients:
            online = [int(c.id) for c in status.clients]
    if request.user.has_perm('b3connect.view_banlist'):
        list = _get_banlist(request)
    else:
        list = []
    return {'client': client, 'status': online, 'banlist': list}

def _get_banlist(request):
    cache_key = "%s_banlist" % request.server
    list = cache.get(cache_key)
    if list is None:
        #list = load_banlist(settings.SERVERS[request.session.get('server')]['BANLIST'])
        list = []
        cache.set(cache_key, list, 60*60)
    return list
        
@login_required
@cache_page(120*60)
@render('b3portal/client/world_map.html')
def player_map(request):
    from common.utils.geoip import GeoLocation
    countries = {}
    geo = GeoLocation()
    for client in Client.objects.filter(id__gt=1):
        country_name = geo.get_country(client.ip)
        if countries.has_key(country_name):
            count = countries.get(country_name) + 1
        else:
            count = 1
        countries[country_name]=count
    return {'list': countries}

@permission_required_with_403('b3connect.view_group')
@cache_page(15*60)
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
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)
    
    res['client_list']=list        
    return res

@permission_required_with_403('b3connect.view_client')
@cache_page(15*60)
@render('b3portal/client/client_list.html')
@flood
def clientlist(request):
    data = ''
    search = None
    filter = 'name'
    
    if request.GET.has_key('searchall') and request.user.has_perm('b3connect.client_advanced_search'):
        field = request.GET['type']
        data = request.GET['data']
        list = {}
        for server in request.server_list:
            list[server.uuid] = _getclientlist(request, server.uuid)
        return {'list': list, 'field': field, 'data': data}
    elif request.GET.has_key('search') or request.GET.has_key('searchall'):
        search = {}
        for k,v in request.GET.items():
            # there is an odd bug I can't identify
            # sometimes type is passed as ?type
            if k == '?type':
                k = 'type'
            search[k]=v
        search['server']=request.server
        data = search['data']
        filter = search['type']
        search = urllib.urlencode(search)
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
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)
    
    return {'client_list': list, 'filter': filter, 'data': data, 'search': search, 'order_by': get_query_order(clients)}

def _getclientlist(request, server, search = True):

    if request.user.has_perm('b3connect.view_high_level_client'):
        clients = Client.objects.using(server).filter(id__gt=1)
    else:
        clients = Client.objects.using(server).filter(Q(group__level__lt=settings.HIGH_LEVEL_CLIENT) | Q(group__isnull=True), id__gt=1)
    
    if search:
        try:
            field = request.GET['type']
        except MultiValueDictKeyError:
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
            clients = clients.filter(Q(ip__startswith=data) | Q(aliases__ip__startswith=data)).distinct()
    
    if request.GET.has_key('sort'):
        sort = request.GET.get('sort')
        order = request.GET.get('order') or 'asc'
        if order == 'desc':
            sort = "-%s" % sort
        clients = clients.order_by(sort)
        
    if request.GET.has_key('level'):
        if not request.user.has_perm('b3connect.view_group'):
            raise Http403
        if request.GET.get('level'):
            clients = clients.filter(group__level=request.GET.get('level'))
        else:
            clients = clients.filter(group__isnull=True)            
    
    return clients

@permission_required_with_403('b3connect.view_client')
@cache_page(15*60)
@render('b3portal/client/regular_client_list.html')
@flood
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
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)
        
    return {'client_list': list}

@permission_required_with_403('b3connect.add_penalty')
@render('b3portal/client/add_penalty.html')
def addpenalty(request, id, notice=False):
    client = get_object_or_404(Client, id=id, using=request.server)
    if notice:
        frmObj = NoticeForm
    else:
        frmObj = PenaltyForm
    if request.method == 'POST':
        form = frmObj(request.POST)
        if form.is_valid():
            p = Penalty(client=client,
                                       reason=form.cleaned_data['reason'],
                                       time_edit=datetime.datetime.now(),
                                       time_add=datetime.datetime.now(),
                                       admin_id=1)
            if form.Meta.type == 1:
                p.duration=0
                p.type='Notice'
            else:
                if form.cleaned_data['permanent']:
                    p.duration=0
                    p.type='Ban'
                else:
                    p.duration = time2minutes(str(form.cleaned_data['time'])+form.cleaned_data['time_type'])
                    p.type='TempBan'
            p.save()
            messages.success(request, _('Penalty added successfully.'))
            return HttpResponseRedirect(reverse("client_detail",kwargs={'id':id}))
    else:
        form = frmObj()
    return {'form': form, 'client': client}

@permission_required_with_403('b3connect.delete_penalty')
def disablepenalty(request, id):
    penalty = get_object_or_404(Penalty, id=id, using=request.server)
    penalty.inactive = 1
    penalty.save()
    messages.success(request, _('Penalty de-activated successfully.'))
    return HttpResponseRedirect(reverse("client_detail",kwargs={'id':penalty.client.id}))

@permission_required_with_403('b3connect.change_penalty')
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
                p.duration = time2minutes(str(form.cleaned_data['time'])+form.cleaned_data['time_type'])
                p.type='TempBan'
            p.reason = form.cleaned_data['reason']
            p.time_edit=datetime.datetime.now()
            p.save()
            messages.success(request, _('Penalty edited successfully.'))
            return HttpResponseRedirect(reverse("client_detail",kwargs={'id':p.client.id}))
    else:
        if p.duration==0:
            form = PenaltyForm(initial={'permanent': True, 'reason': p.reason})
        else:
            form = PenaltyForm(initial={'permanent': False, 'reason': p.reason,
                                        'time': p.duration,
                                        'time_type': 'm'})
    return {'form': form, 'client': p.client}

@permission_required_with_403('b3connect.register_client')
def change_clientgroup(request, id):
    
    if request.method != 'POST':
        raise Http403

    g = request.POST.get('value')
    if g > '2':
        if not request.user.has_perm('change_client_group'):
            raise Http403
    
    group = get_object_or_404(Group, id=int(g), using=request.server)
    client = get_object_or_404(Client, id=id, using=request.server)
    
    if client.group_id > 0:
        if client.group_id > group.id and not request.user.has_perm('change_client_group'):
            raise Http403
    
    client.group = group
    client.save()
    
    return HttpResponse(str(group), mimetype='plain/text')

@permission_required_with_403('b3connect.view_client')
@cache_page(15*60)
@render('b3portal/client/client_aliases.html')
def more_alias(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    return {'aliases': client.aliases.all(), 'banlist': _get_banlist(request)}

@permission_required_with_403('b3connect.view_high_level_client')
@cache_page(15*60)
@render('b3portal/client/client_adminactions.html')
def more_admactions(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    return {'penalties': client.adminpenalties.all()}

@permission_required_with_403('b3connect.view_client')
@cache_page(15*60)
@render('b3portal/client/client_penalties.html')
def more_ipenalties(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    return {'penalties': client.penalties.inactive()[:20]}

@permission_required_with_403('b3connect.view_client')
@cache_page(15*60)
@render('b3portal/client/client_notices.html')
def more_notices(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    return {'notices': client.penalties.notices()}

def direct(request):
    if request.method != 'POST':
        raise Http403
    pid = request.POST.get('playerid')
    next = request.POST.get('next')
    server = request.POST.get('server')
    try:
        pid = int(pid)
    except:
        messages.error(request, _('You entered an invalid player id.'))
        return HttpResponseRedirect(next)
    try:
        player = Client.objects.using(server).get(id=pid)
    except:
        messages.warning(request, _('Player with id %d not found.' % pid))
        return HttpResponseRedirect(next)
    url = reverse("client_detail",kwargs={'id':player.id})
    return HttpResponseRedirect(url + "?server=%s" % server)
