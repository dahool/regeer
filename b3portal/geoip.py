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
import pygeoip
from django.conf import settings

class GeoLocation:
    
    def __init__(self):
        self.geocity = None
        self.geo = None
        
    def _get_citydat(self):
        if not self.geocity:
            self.geocity = pygeoip.GeoIP(settings.GEOIPCITY_DAT)
        return self.geocity

    def _get_geodat(self):
        if not self.geo:
            self.geo = pygeoip.GeoIP(settings.GEOIP_DAT)
        return self.geo
        
    def get_city(self, ip):
        r = self._get_citydat().record_by_addr(ip)
        try:
            c = r['city']
        except:
            c = r['country_name']
        return c

    def get_country(self, ip):
        return self._get_geodat().country_name_by_addr(ip)