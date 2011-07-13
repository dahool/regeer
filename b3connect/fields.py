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