# -*- coding: utf-8 -*-
"""Copyright (c) 2011 Sergio Gabriel Teves
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
from django.template import Node, NodeList, resolve_variable, TemplateSyntaxError
import re

register = template.Library()

@register.tag(name='ifvalidguid')
def isvalidguid(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 2:
        raise TemplateSyntaxError, "%r takes one argument" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
        
    object = bits[1]
                                
    return IfValidGuidNode(object, nodelist_true, nodelist_false)

class IfValidGuidNode(Node):
    def __init__(self, object, nodelist_true, nodelist_false):
        self.object, self.nodelist_true, self.nodelist_false = object, nodelist_true, nodelist_false

    def __repr__(self):
        return "<FfPluginInstalledNone>"

    def render(self, context):
        guid = resolve_variable(self.object,context)
        request = context['request']
        server_list = request.server_list
        server = None
        for s in server_list:
            if request.server == s.uuid:
                server = s
                break
            
        if server and server.game in ('q3a', 'oa081','iourt41','smg','smg11','etpro','q3a'):
            r = re.match('^[A-F0-9]{32}$', guid) 
        elif server and server.game in ('moh','bfbc2'):
            r = re.match('^EA_[a-f0-9]{32}$', guid, re.IGNORECASE)
        elif server and server.game in ('alt',):
            r = re.match('^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', guid, re.IGNORECASE)
        else:
            r = False
    
        if r:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context) 
    