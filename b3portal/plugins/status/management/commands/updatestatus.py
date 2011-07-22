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
from django.core.management.base import BaseCommand
from b3portal.plugins.status.models import ServerStatus, StatusClient, StatusPlugin

class Command(BaseCommand):
    help = 'Read status file and save summary'

    def handle(self, *args, **options):
        for conf in StatusPlugin.objects.all():
            self.stdout.write("Processing %s ...\n" % conf.server)
            try:
                status = conf.get_status()
            except Exception, e:
                self.stderr.write("Error processing %s: %s\n" % (conf.location, str(e)))
            else:
                if status.map:
                    s = ServerStatus.objects.create(map=status.map,
                                                    server=conf.server)
                    if status.totalClients > 0:
                        for client in status.clients:
                            if client.id:
                                StatusClient.objects.create(status=s,
                                                            client_id=client.id)
                                
            self.stdout.write("Processed %s ...\n" % conf.server)
        self.stdout.write('Done.\n')