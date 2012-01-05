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
from django.contrib.contenttypes.models import ContentType
from b3portal import appsettings

class Command(BaseCommand):
    help = 'Initialize Application Permissions'

    def handle(self, *args, **options):
        
        self.stdout.write("Initializing Application Permissions ...\n")
        
        for ctypeKey, perms in appsettings.APP_PERMISSION.items():
            for model, perm, title in perms:
                ctype, c = ContentType.objects.get_or_create(name=model.title(),
                                                  app_label=ctypeKey,
                                                  model=model)
                try:
                    Permission.objects.get_or_create(name=title,
                                              codename=perm,
                                              content_type=ctype)
                except Exception, e:
                    self.stdout.write("Error: %s\n" % str(e))
        
        for name, perms in appsettings.APP_GROUP_PERMISSION:
            self.stdout.write("Updating %s...\n" % name)
            g, c = Group.objects.get_or_create(name=name)
            for perm in perms:
                try:
                    ps = perm.split('.')
                    if len(ps) == 2:
                        app, code = ps
                        p = Permission.objects.get(
                            codename=code,
                            content_type=ContentType.objects.get(app_label=app)
                        )
                    else:
                        app, model, code = ps
                        p = Permission.objects.get_by_natural_key(code, app, model)
                except Exception, e:
                    self.stdout.write("Error: %s\n" % str(e))
                else:
                    g.permissions.add(p)
                    g.save()
            
        self.stdout.write('Success.\n')