from django.template import Library
from django.conf import settings

register = Library()

def media(path):
    """
    Returns the string contained in the setting ADMIN_MEDIA_PREFIX.
    """
    try:
        from django.conf import settings
    except ImportError:
        return path
    #p = getattr(settings, 'VERSION', '1')
    return settings.MEDIA_URL + path #+ "?v=" + p
register.simple_tag(media)

def style(path):
    return '<link rel="stylesheet" type="text/css" href="%s"/>' % media(path)
register.simple_tag(style)

def jscript(path):
    return '<script type="text/javascript" src="%s"></script>' % media(path)
register.simple_tag(jscript)