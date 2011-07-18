from common.view.decorators import render

from django.views.decorators.cache import cache_page

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

@render('b3portal/index.html')
def home(request):
    if len(request.server_list) == 0:
        return HttpResponseRedirect(reverse("admin:index"))
    return {}