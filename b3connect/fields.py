# -*- coding: utf-8 -*-
"""Copyright (c) 2010,2011 Sergio Gabriel Teves
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
from django.db.models import *
from django.utils.encoding import smart_unicode, force_unicode, smart_str
from django import forms
from django.utils import datetime_safe

import datetime
import time

class EpochDateTimeField(Field):
    __metaclass__ = SubfieldBase

    def get_internal_type(self):
        return "IntegerField"
        
    def to_python(self, value):
        if isinstance(value, datetime.datetime):
            return value
        if value is None or value=="":
            return ""
        if value == -1:
            return value
        try:
            return datetime.datetime.fromtimestamp(float(value))
        except:
            return ""

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if hasattr(value, 'timetuple'):
            return int(time.mktime(value.timetuple()))
        else:
            return value

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        if val is None:
            data = ''
        else:
            d = datetime_safe.new_datetime(val)
            data = d.strftime('%Y-%m-%d %H:%M:%S')
        return data

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.DateTimeField}
        defaults.update(kwargs)
        return super(EpochDateTimeField, self).formfield(**defaults)