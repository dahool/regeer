from django.conf import settings
from django.http import HttpResponse

class ServerDetectMiddleware(object):
    
    def process_request(self, request):
#        if hasattr(request, 'session'):
 #           server = request.session.get('server', None)
        from b3portal.models import Server
        request.__class__.server_list = Server.objects.all()
 
        server = None
        if request.GET.has_key('server'):
            server = request.GET.get('server')
        else:
            if request.POST.has_key('server'):
                server = request.POST.get('server')
        if not server:
            if Server.objects.count() > 0:
                server = Server.objects.all()[0].uuid
        request.__class__.server = server

#    def process_response(self, request, response):
#        if isinstance(response, HttpResponse):
#            from b3portal.models import Server
#            response['server_list'] = Server.objects.all()
#        return response