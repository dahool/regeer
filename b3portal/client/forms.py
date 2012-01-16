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
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES
from common.utils.functions import time2minutes

TIME_CHOICES = (
    ('m', _('Minutes')),
    ('h', _('Hours')),
    ('d', _('Days')),
    ('w', _('Weeks')),
    ('M', _('Month')),
    ('y', _('Years')),
)

MAX_DURATION = 10518960 # 20 years

class CommentForm(forms.Form):
    reason = forms.CharField(max_length=765, label=_('Note'))
        
class NoticeForm(forms.Form):
    
    reason = forms.CharField(max_length=765, label=_('Reason'))

    class Meta:
        type = 1

class PenaltyForm(NoticeForm):
    
    permanent = forms.BooleanField(label=_('Permanent'), required=False) 
    time = forms.IntegerField(min_value=1, label=_('Duration'), required=False)
    time_type = forms.ChoiceField(label=_('Period'), choices=TIME_CHOICES)

    def clean(self):
        cleaned_data = self.cleaned_data
        time = cleaned_data['time']
        if time in EMPTY_VALUES and not cleaned_data['permanent']:
            #raise ValidationError(self.fields['time'].error_messages['required'])
            self._errors["time"] = self.error_class([self.fields['time'].error_messages['required']])
            del cleaned_data['time']
        elif not cleaned_data['permanent']:
            time = time2minutes(str(time)+cleaned_data['time_type'])
            if time == 0:
                self._errors["time"] = self.error_class([_('Invalid duration')])
                del cleaned_data['time']
            elif time > MAX_DURATION:
                self._errors["time"] = self.error_class([_('Duration is too big. Why don\'t you use permanent instead?')])
                del cleaned_data['time']
            else:
                cleaned_data['time'] = time
        return cleaned_data

    class Meta:
        type = 2