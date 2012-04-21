from django.http import HttpResponseForbidden, HttpResponseNotFound,\
    HttpResponse, HttpResponseServerError
from django.template import RequestContext, loader, Context
from django.utils.encoding import smart_str
from django.conf import settings

class HttpResponseUnavailable(HttpResponse):
    status_code = 503

def forbidden(request, exception):
    """Default 403 handler"""
    template_name = getattr(settings, 'ERROR403', '403.html')
    
    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'request_path': request.path_info[1:],
        'reason': smart_str(exception, errors='replace'),
        'settings': settings,
    })
        
    return HttpResponseForbidden(t.render(c))

def not_found(request, exception):
    """404 handler"""
    
    template_name = getattr(settings, 'ERROR404', '404.html')
    try:
        tried = exception.args[0]['tried']
    except (IndexError, TypeError):
        tried = []
    else:
        if not tried:
            tried = ''

    t = loader.get_template(template_name)
    c = Context({
        'request_path': request.path_info[1:], # Trim leading slash
        'urlpatterns': tried,
        'reason': smart_str(exception, errors='replace'),
        'request': request,
        'settings': settings,
    })
    return HttpResponseNotFound(t.render(c))

def unavailable(request, exception):
    """503 handler"""

    template_name = getattr(settings, 'ERROR503', '503.html')

    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'request_path': request.path_info[1:],
        'reason': smart_str(exception, errors='replace'),
        'settings': settings,
    })
    return HttpResponseUnavailable(t.render(c))
    
def general_error(request, exception):
    """500 special handler"""

    template_name = getattr(settings, 'ERROR500', '500.html')

    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'request_path': request.path_info[1:],
        'reason': smart_str(exception, errors='replace'),
        'settings': settings,
    })
    return HttpResponseServerError(t.render(c))