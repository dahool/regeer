# -*- coding: utf-8 -*-
"""Copyright (c) 2012 Sergio Gabriel Teves
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
from django.forms import fields
from django.forms import widgets
from django.utils import html
from django.utils.encoding import force_unicode
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

class CommandButtonWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        return '<input type="button" name="command" value="%s">' % (html.escape(name))

class CommandButtonField(fields.Field):
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        kwargs["widget"] = CommandButtonWidget
        super(CommandButtonWidget, self).__init__(*args, **kwargs)

    def clean(self, value):
        return value
      
class InputWidget(widgets.TextInput):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        return mark_safe(u'<input%s />&nbsp;<input type="button" name="command" alt="%s" value="%s">' % (flatatt(final_attrs), final_attrs['id'], self.label))

class SelectWidget(widgets.Select):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(u'</select>')
        output.append(u'&nbsp;<input type="button" name="command" alt="%s" value="%s">' % (final_attrs['id'], self.label))
        return mark_safe(u''.join(output))
          
class InputField(fields.CharField):
    
    def __init__(self, *args, **kwargs):
        self.widget = InputWidget()
        lbl = kwargs.pop('buttonlabel', None)
        self.blank = kwargs.pop('blank', False)
        if lbl:
            self.widget.label = lbl
        else:
            self.widget.label = _('Set')
        super(InputField, self).__init__(*args, **kwargs)
    
class SelectField(fields.ChoiceField):
    
    def __init__(self, *args, **kwargs):
        self.widget = SelectWidget()
        lbl = kwargs.pop('buttonlabel', None)
        self.blank = kwargs.pop('blank', False)
        if lbl:
            self.widget.label = lbl
        else:
            self.widget.label = _('Set')
        super(SelectField, self).__init__(*args, **kwargs)
    