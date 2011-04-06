from django.shortcuts import render_to_response
from django.conf import settings

class AgentRejectMiddleware(object):
    
    def process_request(self, request):
        if 'HTTP_USER_AGENT' in request.META:
            for user_agent_regex in settings.BLOCK_USER_AGENTS:
                if user_agent_regex.search(request.META['HTTP_USER_AGENT']):
                    return render_to_response('ieblock.html')
        return None