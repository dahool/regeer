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
from b3portal.permission.utils import has_any_server_perms

register = template.Library()

@register.tag(name='ifperm')
def ifperm(parser, token):
    '''
    check if user has permission in passed server
    
    {% ifperm user server 'permission' 'permission' %}
    '''
    bits = list(token.split_contents())
    if len(bits) < 4:
        raise TemplateSyntaxError, "%r takes at least 4 arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
            
    return IfPermNode(bits[1], bits[2], bits[3:], nodelist_true, nodelist_false)

class IfPermNode(Node):
    def __init__(self, user, server, perms, nodelist_true, nodelist_false):
        self.user, self.perms, self.server, self.nodelist_true, self.nodelist_false = user, perms, server, nodelist_true, nodelist_false 

    def __repr__(self):
        return "<IfPermNode>"

    def render(self, context):
        user = resolve_variable(self.user, context)
        server = resolve_variable(self.server, context)
        
        perms = []
        for perm in self.perms:
            try:
                perms.append(resolve_variable(perm, context))
            except:
                pass
        if has_any_server_perms(user, perms, server):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)