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
from django import template
from django.template.defaultfilters import stringfilter
from django.template import Node, Template, Context, NodeList, VariableDoesNotExist, resolve_variable, TemplateSyntaxError

import logging
import re
import urllib

logger = logging.getLogger('regeer')

register = template.Library()

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9]+(?:-*[A-Z0-9]+)*\.)+[A-Z]{2,6}$', re.IGNORECASE)

color_re = re.compile(r'\^[0-9]')

@register.filter
@stringfilter
def hidemail(text):
    m = email_re.match(text)
    if m:
        return u"%s..." % m.group(1)
    return text

@register.filter
@stringfilter
def clean_colors(text):
    return color_re.sub('',text)

@register.filter
def sort(list, arg=None):
    if arg:
        return sorted(list, key=lambda x: getattr(x, arg))
    return sorted(list)

@register.filter
@stringfilter
def maskip(text):
    from common.utils.validators import is_valid_ip
    m = is_valid_ip(text)
    if m: 
        return ".".join(m.groups()[0:3]+('*',))
    return "-"

@register.filter
@stringfilter
def baseip(text):
    from common.utils.validators import is_valid_ip
    m = is_valid_ip(text)
    if m: 
        return ".".join(m.groups()[0:3]+('0',))
    return "-"

@register.tag(name='makeurl')
def do_makeurl(parser, token):
    '''
    Generate url from key=value pair
    
        {% makeurl urlstring key1=param1 key2='string2' .... %}
    '''
    args = token.split_contents()
    tag_name = args[0]
    url = args[1]
    params = args[2:]
    if len(params) == 0: raise TemplateSyntaxError, "%r missing url params" % tag_name
    pm = {}
    for p in params:
        k, v = p.split('=')
        pm[k] = parser.compile_filter(v)
    return MakeUrlNode(parser.compile_filter(url), pm)    

class MakeUrlNode(template.Node):
    
    def __init__(self, url, params):
        self.url, self.params = url, params

    def __repr__(self):
        return "<MakeUrlNode>"

    def render(self, context):
        try:
            url = self.url.resolve(context)
            params = dict((k, v.resolve(context)) for k, v in self.params.items())  
        except Exception, e:
            logger.exception("MakeUrlNode <%s>" % str(e))
            return ''
        p = urllib.urlencode(params)
        if url.find('?') == -1:
            url += '?'
        else:
            url += '&'
        url += '%s' % p
        return url