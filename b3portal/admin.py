# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin

from models import Map, UserProfile, Server, Plugins

admin.site.unregister(Site)
admin.site.unregister(User)
admin.site.register(Map)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.register(User, UserProfileAdmin)
admin.site.register(Server)
admin.site.register(Plugins)