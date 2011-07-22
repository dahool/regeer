# -*- coding: utf-8 -*-
"""Copyright (c) 2010,2011 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from urllib import quote

from b3portal.models import Server

def _get_server(obj):
    if isinstance(obj, Server):
        return obj
    return Server.objects.get(pk=obj)
def has_server_perm(user, perm, obj):
    """/
    This fallback to general perms if not object perm is found
    """
    if user.is_anonymous(): return False
    if user.has_perm(perm, _get_server(obj)):
        return True
    return user.has_perm(perm)

def has_server_perms(user, perm_list, obj):
    """/
    This fallback to general perms if not object perm is found
    """
    if user.is_anonymous(): return False
    if user.has_perms(perm_list, _get_server(obj)):
        return True
    return user.has_perms(perm_list)

def has_any_server_perms(user, perm_list, obj):
    """/
    This fallback to general perms if not object perm is found
    """
    if user.is_anonymous(): return False
    srv = _get_server(obj)
    for perm in perm_list:
        if has_server_perm(user, perm, srv):
            return True
    return False

def has_server(user, obj):
    """/
    Check if the user has any kind of permission in the passed object
    """
    if user.is_anonymous(): return False
    if user.is_superuser: return True
    if user.server_permissions.filter(server=obj).count() > 0:
        return True
    # if we have any kind of global permission, this worth for all servers
    return user.has_module_perms('b3connect')
        
def server_permission_required_with_403(perm, login_url=None):
    """/
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page or rendering a 403 as necessary.
    """

    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL
        
    def _check_permission(view_func):
        def _checklogin(request, *args, **kwargs):
            if request.user.is_superuser or has_server_perm(request.user, perm, request.server):
                return view_func(request, *args, **kwargs)
            elif not request.user.is_authenticated():
                return HttpResponseRedirect('%s?%s=%s' % (login_url, REDIRECT_FIELD_NAME, quote(request.get_full_path())))
            else:
                resp = render_to_response('403.html', context_instance=RequestContext(request))
                resp.status_code = 403
                return resp
        _checklogin.__doc__ = view_func.__doc__
        _checklogin.__dict__ = view_func.__dict__
        return _checklogin
    return _check_permission
