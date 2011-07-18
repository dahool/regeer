from django import template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_for_escaping

register = template.Library()

@register.simple_tag
def simpleerror(field):
    if hasattr(field,'errors') and field.errors:
        message = u','.join([u'%s' % force_unicode(e) for e in field.errors])
        message = mark_for_escaping(message) 
    else:
        return False
    return message
    
@register.inclusion_tag('tags/error.html')
def error(field):
    if hasattr(field,'errors') and field.errors:
        message = u','.join([u'%s' % force_unicode(e) for e in field.errors])
        message = mark_for_escaping(message) 
    else:
        return {'message': None}
    return {'message': message}

@register.inclusion_tag('tags/formfield.html')
def formfield(field):
    return {'field': field}

@register.inclusion_tag('tags/form.html')
def as_form(entry, showErrors = True):
    showErrors = showErrors in ['true', 'True', True]
    return {'form': entry, 'errors': showErrors}

@register.inclusion_tag('tags/tabform.html')
def as_tabform(entry):
    return {'form': entry}

field_type_class = {'CheckboxInput':'type-check',
                    'Select':'type-select',
                    'RadioInput':'type-check',}

@register.filter
def type(field):
    name = field.field.widget.__class__.__name__
    return field_type_class.get(name) or "type-text"
