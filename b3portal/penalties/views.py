from common.view.decorators import render

from django.db.models import Q

from b3connect.models import Penalty
from django.conf import settings

import time
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from common.decorators import permission_required_with_403

from django.views.decorators.cache import cache_page

import urllib
from django.contrib.auth.decorators import login_required
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

@permission_required_with_403('b3connect.view_penalty')
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

@permission_required_with_403('b3connect.view_penalty')
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

@permission_required_with_403('b3connect.view_notices')
@cache_page(30*60)
@render('b3portal/penalties/notice_list.html')
def notice_list(request):
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