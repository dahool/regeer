from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.template import RequestContext, loader, Context
from django.utils.encoding import smart_str
from django.conf import settings

def forbidden(request, template_name='403.html'):
    """Default 403 handler"""
    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request)))

def not_found(request, exception, template_name='404.html'):

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