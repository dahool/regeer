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
    
    dbpasswd = forms.RegexField(label=_("Database Password"),
                                widget=forms.widgets.PasswordInput(attrs={'autocomplete':'off'}),
                                required=False,
                                max_length=100,
                                regex=r"^[-!\"#$%&'()*+,./:;<=>?@[\\\]_`{|}~a-zA-Z0-9]+$",
                                error_message = _("Non ascii chars are forbidden."))
    rcon_passwd = forms.RegexField(label=_("RCON Password"),
                                widget=forms.widgets.PasswordInput(attrs={'autocomplete':'off'}),
                                required=False,
                                max_length=100,
                                regex=r"^[-!\"#$%&'()*+,./:;<=>?@[\\\]_`{|}~a-zA-Z0-9]+$",
                                error_message = _("Non ascii chars are forbidden."))
            
    def clean_dbpasswd(self):
        pwd = self.cleaned_data.get('dbpasswd')
        if not pwd:
            if self.instance and self.instance.password:
                pwd = self.instance.password
        
        if not pwd: raise forms.ValidationError(forms.Field.default_error_messages['required'])
        return pwd

    def clean(self):
        data = self.cleaned_data
        rcon_ip = data.get('rcon_ip')
        rcon_port = data.get('rcon_port')
        rcon_pwd = data.get('rcon_passwd')
        
        if self.instance and not rcon_pwd:
            rcon_pwd = self.instance.rcon_password
        
        if not (rcon_ip and rcon_port and rcon_pwd) and (rcon_ip or rcon_port or rcon_pwd):
            raise forms.ValidationError(_("All fields are required for RCON access"));
        
        return data
    
    def save(self, commit=False):
        p = super(ServerForm, self).save(False)
        data = self.cleaned_data
        if data.get('dbpasswd'):
            p.password = data.get('dbpasswd')
        if data.get('rcon_passwd'):
            p.rcon_password = data.get('rcon_passwd')
        if commit:
            p.save()
        return p

    class Meta:
        model = Server
        exclude = ("uuid","rcon_password", "password")
