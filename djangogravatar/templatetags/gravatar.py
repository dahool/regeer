# -*- coding: utf-8 -*-
"""Copyright (c) 2010 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
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
