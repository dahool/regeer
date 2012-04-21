from django.http import HttpResponseForbidden, Http404
from common.middleware.views import forbidden, not_found, unavailable, general_error
from common.middleware.exceptions import Http403, Http503

class HttpErrorMiddleware(object):
         
    def process_exception(self, request, exception):
        if isinstance(exception, Http403):
            return forbidden(request, exception)
        elif isinstance(exception, Http404):
            return not_found(request, exception)
        elif isinstance(exception, Http503):
            return unavailable(request, exception)
        elif 'OperationalError' == exception.__class__.__name__:
            return unavailable(request, exception[1])
        else:
            return None