from django.core.urlresolvers import reverse

def urlreverse(viewname, server, urlconf=None, args=None, kwargs=None, prefix=None, current_app=None):
    url = reverse(viewname, urlconf, args, kwargs, prefix, current_app)
    return url + "?server=%s" % server