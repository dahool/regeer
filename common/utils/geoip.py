import pygeoip
from django.conf import settings
import os
from pygeoip import GeoIPError

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
        r = self.get_city_detail(ip)
        try:
            c = r['city']
        except:
            c = r['country_name']
        return c

    def get_city_detail(self, ip):
        return self._get_citydat().record_by_addr(ip)
    
    def get_country(self, ip):
        return self._get_geodat().country_name_by_addr(ip)