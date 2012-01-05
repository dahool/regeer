# -*- coding: utf-8 -*-
"""Copyright (c) 2009 Sergio Gabriel Teves
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
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.forms.widgets import TextInput, HiddenInput

admin.site.unregister(User)

class ReadOnlyInput(TextInput):

    def __init__(self, attrs=None, render_value=True):
        super(ReadOnlyInput, self).__init__(attrs)
        self.render_value = render_value

    def render(self, name, value, attrs=None):
        if not self.render_value: value=None
        if not attrs: attrs={}
        attrs['readonly']="readonly"
        return super(ReadOnlyInput, self).render(name, value, attrs)

class UserForm(UserChangeForm):
    username = forms.CharField(widget=ReadOnlyInput);
    password = forms.CharField(widget=HiddenInput);

class UserAdminForm(UserAdmin):
    form = UserForm
    
admin.site.register(User, UserAdminForm)