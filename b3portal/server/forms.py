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
from django import forms
from django.forms import ModelForm
from b3portal.models import Server
from django.utils.translation import ugettext_lazy as _

class ServerForm(ModelForm):
    
    password = forms.RegexField(label=_("Database Password"),
                                widget=forms.widgets.PasswordInput(attrs={'autocomplete':'off'}),
                                required=True,
                                max_length=100,
                                regex=r"^[-!\"#$%&'()*+,./:;<=>?@[\\\]_`{|}~a-zA-Z0-9]+$",
                                error_message = _("Non ascii chars are forbidden."))
    rcon_password = forms.RegexField(label=_("RCON Password"),
                                widget=forms.widgets.PasswordInput(attrs={'autocomplete':'off'}),
                                required=False,
                                max_length=100,
                                regex=r"^[-!\"#$%&'()*+,./:;<=>?@[\\\]_`{|}~a-zA-Z0-9]+$",
                                error_message = _("Non ascii chars are forbidden."))
            
    def clean(self):
        data = self.cleaned_data
        rcon_ip = data['rcon_ip']
        rcon_port = data['rcon_port']
        rcon_pwd = data['rcon_password']
        
        if not (rcon_ip and rcon_port and rcon_pwd) and (rcon_ip or rcon_port or rcon_pwd):
            raise forms.ValidationError(_("All fields are required for RCON access"));
        
        return data
    
    class Meta:
        model = Server
        exclude = ("uuid")
