from django import template
from common.utils.geoip import GeoLocation

register = template.Library()

geo = GeoLocation()

@register.filter
def geoip(ip):
    r = geo.get_city_detail(ip)
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
    return {'data': data}