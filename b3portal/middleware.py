# -*- coding: utf-8 -*-
"""Copyright (c) 2011-2012 Sergio Gabriel Teves
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
from b3portal.models import Server
from b3portal import init_database_config
from b3portal.permission.utils import has_server
from django.http import Http404

class ServerDetectMiddleware(object):
    
    SERVER_KEY_NAME = 'server'
    
    def process_request(self, request):
        if hasattr(request, 'session'):
            server_list = request.session.get('server_list', None)
        else:
            server_list = None
            
        if not server_list or len(server_list) == 0:
            server_list = Server.objects.all()
            count = Server.objects.count()
            if count == 0:
                return None
            if hasattr(request, 'session'):
                if count > 0:
                    request.session['server_list'] = server_list
        
        request.__class__.server_list = server_list

        server = None
        if request.GET.has_key('server'):
            server = request.GET.get('server')
        else:
            if request.POST.has_key('server'):
                server = request.POST.get('server')
        if not server:
            if request.COOKIES.has_key(self.SERVER_KEY_NAME):
                value = request.COOKIES[self.SERVER_KEY_NAME]
                if value != 'None' and has_server(request.user,value):
                    server = value
            if not server and request.user.is_authenticated() and request.user.server_permissions.all():
                server = request.user.server_permissions.all()[0].server.uuid
            if not server:
                for s in server_list:
                    if s.default:
                        server = s.uuid
                        break
            if not server and len(server_list) > 0:
                server = server_list[0].uuid
        
        server_obj = None
        for s in server_list:
            if s.uuid == server:
                server_obj = s
                break
                
        if not server or not server_obj:                
            raise Http404        
        
        request.__class__.server = server
        request.__class__.server_obj = server_obj
        
    def process_response(self, request, response):
        if response and hasattr(request, 'server'):
            response.set_cookie(self.SERVER_KEY_NAME, request.__class__.server)
        return response
    
class MultiDBMiddleware(object):
    
    def process_request(self, request):
        from django.conf import settings
        if settings.RUNTIME_DB_UPDATE: init_database_config(request)
