# -*- coding: utf-8 -*-
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