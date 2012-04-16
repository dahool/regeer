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
from django import template

register = template.Library()

@register.tag
def current_nav(parser, token):
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    if len(args) == 2:
        return NavSelectedNode(args[1])
    else:
        return NavSelectedNode(args[1], args[2])

class NavSelectedNode(template.Node):
    def __init__(self, url, style='nav-active'):
        self.url = url
        self.style = style

    def render(self, context):
        try:
            path = context['request'].path
            pValue = template.Variable(self.url).resolve(context)
            if (pValue == '/' or pValue == '') and not (path  == '/' or path == ''):
                return ""
            if path.startswith(pValue):
                return self.style
        except:
            pass
        return ""
