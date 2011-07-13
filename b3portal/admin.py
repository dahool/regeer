# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from django.conf import settings

from b3portal.server.forms import ServerForm

from models import Map, UserProfile, Server, Plugins, MapCycle

admin.site.unregister(Site)
admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

class ServerAdmin(admin.ModelAdmin):
    form = ServerForm
    fieldsets = [
        (None,               {'fields': ['name','default']}),
        (_('Database settings'), {'fields': ['engine','hostname','database','user','password']}),
        (_('Game Server'), {'fields': ['rcon_ip','rcon_port', 'rcon_password', 'parser']}),
    ]    
    
 
if (settings.DEBUG):   
    admin.site.register(Map)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(MapCycle)
admin.site.register(Plugins)