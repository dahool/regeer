from models import KnifeStat, NaderStat, FlagStat
from common.view.decorators import render
from django.views.decorators.cache import cache_page
from django.utils.translation import gettext as _
from django.contrib import messages
from django.conf import settings

@cache_page(30*60)
@render('stats/stats.html')
def home(request):
    dp = settings.SERVERS[request.session.get('server')]['PLUGINS']
    res = {}
    if 'flagstats' in dp:
        res['mflags'] = FlagStat.objects.using(request.session.get('server')).all().order_by('-most_capture_score', 'most_capture_timeadd')[:5]
        res['qflags'] = FlagStat.objects.using(request.session.get('server')).all().order_by('quick_capture_score', 'quick_capture_timeadd')[:5]
    if 'knifestats' in dp:
        res['knifers'] = KnifeStat.objects.using(request.session.get('server')).all().order_by('-score','time_add')[:5]
    if 'hestats' in dp:
        res['naders'] = NaderStat.objects.using(request.session.get('server')).all().order_by('-score','time_add')[:5]
    return res
    
@cache_page(30*60)
@render('stats/he_stats.html')
def he_stats(request):
    if not 'hestats' in settings.SERVERS[request.session.get('server')]['PLUGINS']:
        return {}
    return {'list': NaderStat.objects.using(request.session.get('server')).all().order_by('-score','time_add')}

@cache_page(30*60)
@render('stats/kn_stats.html')
def kn_stats(request):
    if not 'knifestats' in settings.SERVERS[request.session.get('server')]['PLUGINS']:
        return {}
    return {'list': KnifeStat.objects.using(request.session.get('server')).all().order_by('-score','time_add')}

@cache_page(30*60)
@render('stats/mflg_stats.html')
def mflg_stats(request):
    if not 'flagstats' in settings.SERVERS[request.session.get('server')]['PLUGINS']:
        return {}
    return {'list': FlagStat.objects.using(request.session.get('server')).all().order_by('-most_capture_score', 'most_capture_timeadd')}

@cache_page(30*60)
@render('stats/qflg_stats.html')
def qflg_stats(request):
    if not 'flagstats' in settings.SERVERS[request.session.get('server')]['PLUGINS']:
        return {}
    return {'list': FlagStat.objects.using(request.session.get('server')).all().order_by('quick_capture_score', 'quick_capture_timeadd')}    