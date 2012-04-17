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
from django.utils.translation import ugettext_lazy as _
from djangoui.widgets import uiSplitDateTimeWidget

class ChatLogSearch(forms.Form):
    
    #name = forms.CharField(max_length=50, label=_('Name/@id'), required=False)
    name = forms.CharField(max_length=10, label=_('@id'), required=False)
    datefrom = forms.SplitDateTimeField(('%d/%m/%Y',),('%H:%M',),
                                    widget=uiSplitDateTimeWidget(date_format="%d/%m/%Y",
                                                                 show_seconds=False),
                                    label=_('From'),
                                    required=False)
    text = forms.CharField(max_length=50, label=_('Text'), required=False, min_length=4)
    dateto = forms.SplitDateTimeField(('%d/%m/%Y',),('%H:%M',),
                                    widget=uiSplitDateTimeWidget(date_format="%d/%m/%Y",
                                                                 show_seconds=False),
                                    label=_('To'), required=False)
    
    @property
    def datetime_from(self):
        if self.cleaned_data['datefrom']:
            df = self.cleaned_data['datefrom']
            return df.strftime('%d/%m/%Y'), df.strftime('%H:%M')
        else:
            return None, None
        
    @property
    def datetime_to(self):
        if self.cleaned_data['dateto']:
            df = self.cleaned_data['dateto']
            return df.strftime('%d/%m/%Y'), df.strftime('%H:%M')
        else:
            return None, None
