from common.view.decorators import render
from b3portal.plugins.map.models import Map
from django.views.decorators.cache import cache_page

@cache_page(60*60)
@render('map/map_list.html')
def maps(request):
    maps = Map.objects.all()
    return {'maps': maps}