from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9]+(?:-*[A-Z0-9]+)*\.)+[A-Z]{2,6}$', re.IGNORECASE)

color_re = re.compile(r'\^[0-9]')

@register.filter
@stringfilter
def hidemail(text):
    m = email_re.match(text)
    if m:
        return u"%s..." % m.group(1)
    return text

@register.filter
@stringfilter
def clean_colors(text):
    return color_re.sub('',text)

@register.filter
def sort(list, arg=None):
    if arg:
        return sorted(list, key=lambda x: getattr(x, arg))
    return sorted(list)

@register.filter
@stringfilter
def maskip(text):
    from common.utils.validators import is_valid_ip
    m = is_valid_ip(text)
    if m: 
        return ".".join(m.groups()[0:3]+('*',))
    return "-"

@register.filter
@stringfilter
def baseip(text):
    from common.utils.validators import is_valid_ip
    m = is_valid_ip(text)
    if m: 
        return ".".join(m.groups()[0:3]+('0',))
    return "-"