from django.conf import settings
from common.view.decorators import render
from django.utils.translation import gettext as _
from common.decorators import permission_required_with_403
from django.views.decorators.cache import cache_page
from plugins.status import get_server_status
from plugins.status.models import ServerStatus

import datetime
from common.collections import OrderedDict
from common.utils.dateutil import datetimeIterator
from common.shortcuts import get_object_or_404
from b3connect.models import Client

@permission_required_with_403('status.view_serverstatus')    
@cache_page(15)
@render('status/game_status.html')
def game_status(request):
    status = get_server_status(request.session.get('server'))
    return {"status": status}

@permission_required_with_403('status.view_serverstatus')    
@cache_page(60*60)
@render('status/client_detail.html')
def client_detail(request, id):
    status = ServerStatus.objects.filter(server=request.session.get('server'),
                                       players__clientid=id)
    client = get_object_or_404(Client, id=id, using=request.session.get('server'))
    return {"client": client,"status": status}

@permission_required_with_403('status.view_serverstatus')    
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
    list = ServerStatus.objects.filter(server=request.session.get('server'),
                                       time_add__gte=from_date,
                                       time_add__lte=to_date) 
    for s in list:
        key = s.time_add.strftime(format).lower()
        if s.totalPlayers > data[key]: 
            data[key] = s.totalPlayers
    return {'list': data}