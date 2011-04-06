from django.conf import settings
from django.http import HttpResponsePermanentRedirect 

class RedirectMiddleware(object):
    
    def process_request(self, request):
#        for redirect_url, redirect_to, expire in settings.PERMANENT_REDIRECT:
#            if redirect_url.search(request.PATH):
#                for group in redirect_url.match(request.PATH).groups.keys(): 
#                    redirect_to = redirect_to.replace(group,)
        pass