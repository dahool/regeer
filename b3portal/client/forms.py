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

TIME_CHOICES = (
    ('m', _('Minutes')),
    ('h', _('Hours')),
    ('d', _('Days')),
    ('w', _('Weeks')),
    ('M', _('Month')),
    ('y', _('Years')),
)

class NoticeForm(forms.Form):
    
    reason = forms.CharField(max_length=765, label=_('Reason'))

    class Meta:
        type = 1

class PenaltyForm(NoticeForm):
    
    permanent = forms.BooleanField(label=_('Permanent'), required=False) 
    time = forms.IntegerField(min_value=1, label=_('Duration'), required=False)
    time_type = forms.ChoiceField(label=_('Period'), choices=TIME_CHOICES)

    def clean_time(self):
        time = self.cleaned_data['time']
        if time in EMPTY_VALUES and not self.cleaned_data['permanent']:
            raise ValidationError(self.fields['time'].error_messages['required'])
        return time

    class Meta:
        type = 2