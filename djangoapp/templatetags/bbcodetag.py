from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
import string
import re

register = template.Library()

@register.inclusion_tag('tags/smileysrender.html')
def smileyrender():
    list = []
    for item in settings.SMILEYS_PACK:
        list.append({'code': item[0],'img': settings.SMILEYS_ROOT + item[1]})
    return {'list': list}

@register.filter
def smiley(value):
    img = '<img src="%s"/>'
    for item in settings.SMILEYS_PACK:
        code = string.replace(string.replace(item[0], "(", "\("),")","\)")
        pattern = r"(?i)%s" % code
        value = re.sub(pattern, img % (settings.SMILEYS_ROOT + item[1]),value)
    return mark_safe(value)    

@register.filter
def bbcode(value):
    """
    Generates (X)HTML from string with BBCode "markup".
    By using the postmark lib from:
    @see: http://code.google.com/p/postmarkup/
    
    """ 
    try:
        from postmarkup import render_bbcode
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in {% bbcode %} filter: The Python postmarkup library isn't installed."
        return force_unicode(value)
    else:
        return mark_safe(render_bbcode(value))
bbcode.is_save = True

@register.filter
def strip_bbcode(value):
    """ 
    Strips BBCode tags from a string
    By using the postmark lib from: 
    @see: http://code.google.com/p/postmarkup/
    
    """ 
    try:
        from postmarkup import strip_bbcode
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in {% bbcode %} filter: The Python postmarkup library isn't installed."
        return force_unicode(value)
    else:
        return mark_safe(strip_bbcode(value))
bbcode.is_save = True