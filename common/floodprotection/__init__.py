try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback. 
from django.utils.decorators import available_attrs    
from django.shortcuts import render_to_response
from django.template import RequestContext
import settings
import urllib
import time

def flood(view_func, seconds=30, template='flood.html'):
    """Flood protection mechanism
    """
    if not seconds:
        seconds = settings.FLOOD_TIMEOUT
    if not template:
        template = settings.FLOOD_TEMPLATE
    
    def _wrapped_view(request, *args, **kwargs):
        var = "flood-%s.%s" % (view_func.__module__,view_func.__name__)
        last_access = request.session.get(var, None)
        timeout = seconds
        if last_access:
            if request.user.is_authenticated():
                if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                if request.user.groups.all():
                    flood_time = None
                    for g in request.user.groups.all():
                        if g.floodsettings.all():
                            if flood_time is None or g.floodsettings.get().timeout < flood_time:
                                flood_time = g.floodsettings.get().timeout
                    if flood_time:
                        timeout = flood_time
            if (last_access + timeout)>int(time.time()):
                path = request.path
                if request.GET:
                    path += "?%s" % urllib.urlencode(request.GET)
                return render_to_response(template, 
                                          {'path': path}, 
                                          context_instance=RequestContext(request))
        request.session[var] = int(time.time())
        return view_func(request, *args, **kwargs)
    return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)