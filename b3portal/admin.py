# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from django.conf import settings

from b3portal.server.forms import ServerForm

from models import UserProfile, Server

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
    
    def save_model(self, request, obj, form, change):
        super(ServerAdmin, self).save_model(request, obj, form, change)
        obj.save()
        if obj.default:
            q = Server.objects.filter(default=True).exclude(pk=obj.pk)
            if q.count() > 0:
                q.update(default=False)
                self.message_user(request, _("A new default server has been added."))
            elif change:
                self.message_user(request, _("A default server has been added."))

        if hasattr(request, 'session'):
            try:
                del request.session['server_list']
            except:
                pass

admin.site.register(User, UserProfileAdmin)
admin.site.register(Server, ServerAdmin)