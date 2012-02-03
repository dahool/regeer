# -*- coding: utf-8 -*-
"""Copyright (c) 2011 Sergio Gabriel Teves
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
from django.contrib import admin
from b3portal.plugins.status.models import StatusPlugin
from django import forms
from django.utils.translation import ugettext_lazy as _

class StatusPluginForm(forms.ModelForm):
        
    location = forms.CharField(label=_('Status File Location'),
                               help_text=_('Local, ftp and http are supported<br/>For ftp use: ftp://user:password@host:port/file/status.xml<br/>For http use: http://your.url.com/status.xml'),
                               max_length=500,
                               widget=forms.TextInput(attrs={'size':'100'}))

    class Meta:
        model = StatusPlugin
                
class StatusPluginAdmin(admin.ModelAdmin):
    form = StatusPluginForm
        
admin.site.register(StatusPlugin, StatusPluginAdmin)