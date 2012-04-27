# -*- coding: utf-8 -*-
"""Copyright (c) 2010-2012 Sergio Gabriel Teves
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
from django import forms
from b3portal.plugins.ipdb.models import IpdbPlugin
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError


class IpdbPluginForm(forms.ModelForm):
        
    def clean(self):
        data = self.cleaned_data
        server = data['server']
        if server.rcon_ip is None or server.rcon_ip == '':
            raise ValidationError('In order to enable IPDB, you need to fill in Server Ip and port under Game Server tab in server configuration.')
        return data
        
    class Meta:
        model = IpdbPlugin
        

class IpdbPluginAdmin(admin.ModelAdmin):
    form = IpdbPluginForm
                    
admin.site.register(IpdbPlugin, IpdbPluginAdmin)