from models import Follow
from common.view.decorators import render
from common.shortcuts import get_object_or_404
from b3connect.models import Client
from forms import FollowForm
import datetime
from django.utils.translation import gettext as _

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from b3portal.plugins import is_plugin_enabled

from b3portal.permission.utils import server_permission_required_with_403
from b3portal import permissions as perm


@server_permission_required_with_403(perm.FOLLOW_VIEW)
@render('follow/list.html')
def home(request):
    if not is_plugin_enabled(request.server, 'follow'):
        messages.info(request, _('This function is not enabled for this server.'))
        return {'list': None}  
        
    return {'list': Follow.objects.using(request.server).all().order_by('-time_add')}

@server_permission_required_with_403(perm.FOLLOW_ADD)
@render('follow/add.html')
def add(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            p = Follow.objects.using(request.server).create(client=client,
                       reason=_("%(reason)s (by %(user)s)") % {'reason': form.cleaned_data['reason'], 'user': request.user},
                       time_add=datetime.datetime.now(),
                       admin_id=0)
            messages.success(request, _('Follow added successfully.'))
            return HttpResponseRedirect(reverse("client_detail",kwargs={'id':id}))
    else:
        if client.followed.all():
            messages.error(request, _('User already exists.'))
            return HttpResponseRedirect(reverse("client_detail",kwargs={'id':id}))            
        form = FollowForm()
        
    return {'form': form, 'client': client}

@server_permission_required_with_403(perm.FOLLOW_DELETE)
def remove(request, id):
    client = get_object_or_404(Client, id=id, using=request.server)
    if client.followed.all():
        for r in client.followed.all():
            r.delete()
        messages.success(request, _('User removed of the watch list'))    
    else:
        messages.error(request, _('User is not in the watch list'))

    if request.GET.has_key('ls'):
        return HttpResponseRedirect(reverse("follow:home"))
    else:
        return HttpResponseRedirect(reverse("client_detail",kwargs={'id': id}))    
