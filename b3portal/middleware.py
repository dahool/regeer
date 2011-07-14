from b3portal.models import Server
from b3portal import init_database_config

class ServerDetectMiddleware(object):
    
    def process_request(self, request):
        if hasattr(request, 'session'):
            server_list = request.session.get('server_list', None)
        else:
            server_list = None
            
        if not server_list:
            server_list = Server.objects.all()
            if hasattr(request, 'session'):
                if len(server_list)>0:
                    request.session['server_list'] = server_list
        
        request.__class__.server_list = server_list
 
        server = None
        if request.GET.has_key('server'):
            server = request.GET.get('server')
        else:
            if request.POST.has_key('server'):
                server = request.POST.get('server')
        if not server:
            if len(server_list) > 0:
                # find default server
                for s in server_list:
                    if s.default:
                        server = s.uuid
                        break
                if not server:
                    server = server_list[0].uuid
        request.__class__.server = server
        
class MultiDBMiddleware(object):
    
    def process_request(self, request):
        init_database_config(request)
