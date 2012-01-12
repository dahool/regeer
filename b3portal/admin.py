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
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from django.conf import settings

from b3portal.server.forms import ServerForm

from models import UserProfile, Server, ServerPermission
from b3portal.models import ServerBanList

admin.site.unregister(Site)
admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
class ServerPermissionInline(admin.StackedInline):
    extra = 1
    model = ServerPermission

class UserProfileAdmin(UserAdmin):
    inlines = [ServerPermissionInline]

class ServerBanListInline(admin.StackedInline):
    model = ServerBanList
    verbose_name = _('Server Banlist')
    verbose_name_plural = _('Server Banlist')
        
class ServerAdmin(admin.ModelAdmin):
    form = ServerForm
    inlines = [ServerBanListInline]
    fieldsets = [
        (None,               {'fields': [('name','default'),'game','owners']}),
        (_('Database settings'), {'fields': ['hostname','database',('user','dbpasswd')]}),
        (_('Game Server'), {'classes': ('collapse',),
                            'fields': [('rcon_ip','rcon_port'), 'rcon_passwd']}),
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

class ServerPermissionAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)
    
admin.site.register(User, UserProfileAdmin)
admin.site.register(Server, ServerAdmin)

admin.site.register(ServerPermission, ServerPermissionAdmin)

if settings.DEBUG:
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    admin.site.register(Permission)
    admin.site.register(ContentType)