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
from common.utils.geoip import GeoLocation
from django.conf import settings

register = template.Library()

geo = GeoLocation()

@register.filter
def geoip(ip):
    try:
        r = geo.get_city_detail(ip)
    except:
        r = None
    return r
    
@register.inclusion_tag('tags/geoip.html')
def geolocation(ip):
    data = geoip(ip)
    if data:
        try:
            data['city'] = data['city'].decode('ISO-8859-1')
        except:
            data['city'] = None
        data['img'] = 'images/flag/%s.gif' % data['country_code'].lower()
    return {'data': data, 'STATIC_URL': settings.STATIC_URL}

@register.inclusion_tag('tags/geoip.html')
def geocountry(ip):
    data = geoip(ip)
    if data:
        data['city'] = None
        data['img'] = 'images/flag/%s.gif' % data['country_code'].lower()
    return {'data': data, 'STATIC_URL': settings.STATIC_URL}