from django.conf import settings
from django.http import HttpResponse

class ServerDetectMiddleware(object):
    
    def process_request(self, request):
        if hasattr(request, 'session'):
            server = request.session.get('server', None)        
        if request.GET.has_key('server'):
            server = request.GET.get('server')
        else:
            if request.POST.has_key('server'):
                server = request.POST.get('server')
        if not server:
            server = 'default'        
        request.session['server']=server
        request.__class__.server_list = [{'DB': k, 'NAME': v['TITLE']} for (k,v) in settings.SERVERS.items()]

    def process_response(self, request, response):
        if isinstance(response, HttpResponse):
            if request.session.has_key('server'):
                response['server'] = request.session['server']
        return response