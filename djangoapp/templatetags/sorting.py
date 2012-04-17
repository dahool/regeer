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
from common.utils.urlutils import extract_params, serialize_params, parse_params

register = template.Library()

@register.inclusion_tag('tags/sorting.html')
def sortheader(data, name, params=None, url=None, style=None):
    if not style:
        style = 'sorted'
    if data and data[:1]=='-':
        order = 'd'
        data = data[1:]
    else:
        order = 'a'
    if url:
        if url.find('?') != -1:
            url, urlpar = extract_params(url) 
            params.update(urlpar)
    else:
        url = ''
    if params:
        if not isinstance(params, dict):
            params = parse_params(params)
    else:
        params = {}
    params['sort']=name
    try:
        del params['order']
    except KeyError:
        pass
    try:
        del params['page']
    except KeyError:
        pass    
    url += '?%s' % serialize_params(params)
    return {'style': style, 'order': order, 'data': data, 'name': name, 'url': url}