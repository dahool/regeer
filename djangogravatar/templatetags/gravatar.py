import urllib
from django import template
from djangogravatar import settings
from djangogravatar.util import email_hash

register = template.Library()

@register.simple_tag
def gravatar(email, style="avatar", size=settings.GRAVATAR_SIZE):
    url = settings.GRAVATAR_URL + "avatar/%(url)s?%(ops)s" % {'url': email_hash(email),
                                                              'ops': urllib.urlencode({
                                                                's': size,
                                                                'd': settings.GRAVATAR_DEFAULT
                                                                })}
    return ("""<img class="%(style)s" src="%(url)s" width="%(size)spx" height="%(size)spx" border="0" alt="gravatar" />""" % 
                {'url': url,
                 'size': size,
                 'style': style})
