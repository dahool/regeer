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
from b3portal.utils.engine import check_guid
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
        return "<IfValidGuidNode>"

    def render(self, context):
        guid = resolve_variable(self.object,context)
        request = context['request']
        server_list = request.server_list
        server = None
        for s in server_list:
            if request.server == s.uuid:
                server = s
                break
        
        if server and check_guid(server.game, guid):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context) 
        
@register.tag(name='ifiplisted')
def ifiplisted(parser, token):
    '''
    {% ifiplisted list 127.0.0.1 %}
    {% endifiplisted %}
    '''
    try:
        tagname, lista, value = token.split_contents()
    except:
        raise TemplateSyntaxError, "%r takes two arguments" % token.split_contents()[0]
    end_tag = 'end' + tagname
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfIpListedNode(parser.compile_filter(lista), parser.compile_filter(value), nodelist_true, nodelist_false)

class IfIpListedNode(Node):
    
    def __init__(self, lista, value, nodelist_true, nodelist_false):
        self.lista, self.value, self.nodelist_true, self.nodelist_false = lista, value, nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfIpListedNode>"

    def render(self, context):
        from gameutils import ip_to_decimal, ip_find_tupple
        lista = self.lista.resolve(context)
        value = self.value.resolve(context)
        if value and lista and ip_find_tupple(lista, ip_to_decimal(value)):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)    

@register.tag(name='loadserver')
def loadserver(parser, token):
    content = token.split_contents()
    if len(content) == 2:
        tag_name, varname = content
    else:
        raise TemplateSyntaxError, "%r takes one argument" % token.split_contents()[0]
    return LoadServerNode(varname)    

class LoadServerNode(template.Node):
    
    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return "<LoadServerNode>"

    def render(self, context):
        try:
            server = context['request'].server
            serverList =  context['request'].server_list
            currentServer = None
            if serverList and server:
                for s in serverList:
                    if s.uuid == server:
                        currentServer = s
                        break
            if currentServer:
                context[self.varname] = currentServer
            else:
                context[self.varname] = None
        except:
            pass
        return ''
