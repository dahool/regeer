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
