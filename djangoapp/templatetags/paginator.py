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
from django.conf import settings
from common.utils.urlutils import extract_params, serialize_params, parse_params

import re

register = template.Library()

LEADING_PAGE_RANGE_DISPLAYED = getattr(settings, 'LEADING_PAGE_RANGE_DISPLAYED', 8)
TRAILING_PAGE_RANGE_DISPLAYED = getattr(settings, 'TRAILING_PAGE_RANGE_DISPLAYED', LEADING_PAGE_RANGE_DISPLAYED)
LEADING_PAGE_RANGE = getattr(settings, 'LEADING_PAGE_RANGE', 3)
TRAILING_PAGE_RANGE = getattr(settings, 'TRAILING_PAGE_RANGE', LEADING_PAGE_RANGE)
NUM_PAGES_OUTSIDE_RANGE = getattr(settings, 'PAGES_OUTSIDE_RANGE', 2)
ADJACENT_PAGES = getattr(settings, 'PAGES_OUTSIDE_RANGE', 4)

PAGE_RE = re.compile('[\&]?(page=[0-9]+)')

@register.inclusion_tag('tags/pagination.html')
def paginate(data, params=None):
    url = ''
    if params:
        if params.find("?"):
            url, params = extract_params(params) 
        else:
            params = parse_params(params)
    else:
        params = {}
    url += '?%s' % serialize_params(params)
    return {'data': data, 'params': url}

@register.inclusion_tag('tags/pagination_page.html', takes_context = True)
def paginatepage(context, data, params=None):
    " Initialize variables "
    in_leading_range = in_trailing_range = False
    pages_outside_leading_range = pages_outside_trailing_range = range(0)
 
    tagContext={'pages': data.paginator.num_pages, 'page': data.number}
    
    if (tagContext["pages"] <= LEADING_PAGE_RANGE_DISPLAYED):
        in_leading_range = in_trailing_range = True
        page_numbers = [n for n in range(1, tagContext["pages"] + 1) if n > 0 and n <= tagContext["pages"]]           
    elif (tagContext["page"] <= LEADING_PAGE_RANGE):
        in_leading_range = True
        page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= tagContext["pages"]]
        pages_outside_leading_range = [n + tagContext["pages"] for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
    elif (tagContext["page"] > tagContext["pages"] - TRAILING_PAGE_RANGE):
        in_trailing_range = True
        page_numbers = [n for n in range(tagContext["pages"] - TRAILING_PAGE_RANGE_DISPLAYED + 1, tagContext["pages"] + 1) if n > 0 and n <= tagContext["pages"]]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
    else: 
        page_numbers = [n for n in range(tagContext["page"] - ADJACENT_PAGES, tagContext["page"] + ADJACENT_PAGES + 1) if n > 0 and n <= tagContext["pages"]]
        pages_outside_leading_range = [n + tagContext["pages"] for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]

    # include server param if exists
    url = None
    if params:
        if params.find('?') != -1:
            url, params = extract_params(params) 
        else:
            params = parse_params(params)
        try:
            del params['page']
        except:
            pass
    else:
        params = {}

    request = context['request']
    if request.server:
        if not params.has_key('server'):
            params['server'] = request.server
    
    if url:
        pdata = '%s?%s' % (url, serialize_params(params))
    else:
        pdata = '?%s' % serialize_params(params)
     
    return {'data': data,
            'numbers': page_numbers,
            'in_leading_range': in_leading_range,
            'page_numbers': page_numbers,
            'pages_outside_trailing_range': pages_outside_trailing_range,
            'in_trailing_range': in_trailing_range,
            'pages_outside_leading_range': pages_outside_leading_range,
            'params': pdata}