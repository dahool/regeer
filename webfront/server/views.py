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
from webfront.client.forms import PenaltyForm
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

from webfront.models import Server
from webfront.server.forms import ServerForm

# TODO permissions
@permission_required_with_403('b3connect.change_server')
@render('webfront/server/form.html')
def edit_server(request, slug = None):
    if request.method == 'POST':
        if slug:
            server = get_object_or_404(Server, slug=slug)
            form = ServerForm(request.POST, instance=server)
        else:
            server = None
            form = ServerForm(request.POST)
        if form.is_valid():
            s = form.save(True)
            if slug:
                messages.success(request, _('Server changed successfully.'))
            else:
                messages.success(request, _('Server added successfully.'))
            return HttpResponseRedirect(reverse("server_detail",kwargs={'slug':s.slug}))
    else:
        if slug:
            server = get_object_or_404(Server, slug=slug)
            form = ServerForm(instance=server)
        else:
            server = None
            form = ServerForm()
    return {'form': form, 'server': server}

@render('webfront/server/list.html')
def list(request):
    return {'list': Server.objects.all()}