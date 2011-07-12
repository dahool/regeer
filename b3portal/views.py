from common.view.decorators import render

from b3portal.models import Map

from django.views.decorators.cache import cache_page

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

@cache_page(5*60)
@render('b3portal/index.html')
def home(request):
    if len(request.server_list) == 0:
        return HttpResponseRedirect(reverse("admin:index"))
    return {}

@cache_page(60*60)
@render('b3portal/map_list.html')
def maps(request):
    maps = Map.objects.all()
    return {'maps': maps}