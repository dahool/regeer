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
from b3portal.plugins import is_plugin_installed, is_plugin_enabled

register = template.Library()

@register.tag(name='ifplugininstalled')
def ifinstalled(parser, token):
    '''
    check if the given plugin is installed.
    '''
    bits = list(token.split_contents())
    if len(bits) < 1:
        raise TemplateSyntaxError, "%r takes at least one argument" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
        
    object = bits[1]
                                
    return IfInstalledNode(object, nodelist_true, nodelist_false)

class IfInstalledNode(Node):
    def __init__(self, object, nodelist_true, nodelist_false):
        self.object, self.nodelist_true, self.nodelist_false = object, nodelist_true, nodelist_false

    def __repr__(self):
        return "<FfPluginInstalledNone>"

    def render(self, context):
        obj = resolve_variable(self.object,context)
        request = context['request']
        
        server_list = request.server_list
        m = False
        for s in server_list:
            if is_plugin_enabled(s, obj):
                m = True
                break
        
        if m:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context) 

@register.tag(name='ifpluginenabled')
def ifenabled(parser, token):
    '''
    check if the given plugin is enabled.
    '''
    bits = list(token.split_contents())
    if len(bits) < 1:
        raise TemplateSyntaxError, "%r takes at least one argument" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
        
    object = bits[1]
    try:
        server = bits[2]
    except:
        server = None
        
    return IfEnabledNode(object, server, nodelist_true, nodelist_false)

class IfEnabledNode(Node):
    def __init__(self, object, server, nodelist_true, nodelist_false):
        self.object, self.server, self.nodelist_true, self.nodelist_false = object, server, nodelist_true, nodelist_false

    def __repr__(self):
        return "<FfPluginEnabledNone>"

    def render(self, context):
        obj = resolve_variable(self.object,context)
        if not self.server:
            request = context['request']
            server = request.server
        else:
            server = resolve_variable(self.server,context)
        if is_plugin_enabled(server, obj):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)     