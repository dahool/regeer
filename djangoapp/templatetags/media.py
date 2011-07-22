# -*- coding: utf-8 -*-
"""Copyright (c) 2009 Sergio Gabriel Teves
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