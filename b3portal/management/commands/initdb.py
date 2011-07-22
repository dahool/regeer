# -*- coding: utf-8 -*-
"""Copyright (c) 2010,2011 Sergio Gabriel Teves
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
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

GROUPS = [('Moderator',['b3connect.group.view_group',
                        'b3connect.client.view_client',
                        'b3connect.client.register_client',
                        'b3connect.client.regular_client',
                        'b3connect.client.regular_client',
                        'b3connect.alias.view_aliases',
                        'b3connect.penalty.view_penalty',
                        'b3connect.penalty.view_notices',
                        'b3connect.penalty.view_banlist',
                        'b3connect.penalty.add_notice',
                        'status.serverstatus.view_serverstatus',
                        'follow.follow.view_follow',
                        'chatlog.chatlog.view_chat'])]

class Command(BaseCommand):
    help = 'Init Permission Groups'

    def handle(self, *args, **options):
        
        for name, perms in GROUPS:
            self.stdout.write("Processing %s...\n" % name)
            g, c = Group.objects.get_or_create(name=name)
            for perm in perms:
                app, model, code = perm.split('.')
                try:
                    p = Permission.objects.get_by_natural_key(code, app, model)
                except:
                    pass
                else:
                    g.permissions.add(p)
                    g.save()
            
        self.stdout.write('Success.\n')
        