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
from b3portal.plugins.map.models import MapPlugin, Map
from common.utils.file import getfile

class Command(BaseCommand):
    help = 'Fill maps table'

    def handle(self, *args, **options):

        self.stdout.write("Cleaning existing data...\n")
        for m in Map.objects.all():
            m.delete()

        i=0
        for mapcycle in MapPlugin.objects.all():
            mfile = None
            try:
                mfile = getfile(mapcycle.location)
                if mfile:
                    tmaps = mfile.read().strip().splitlines()
                    if tmaps:
                        _settings = False
                        for m in tmaps:
                            if m == '}':
                                _settings = False
                                continue
                            elif m == '{':
                                _settings = True
                            if not _settings:
                                if m != '':
                                    Map.objects.create(name=m, server=mapcycle.server)
                                    i+=1
                else:
                    self.stderr.write('Unable to read file %s\n' % mapcycle.location)
            except Exception, e:
                self.stderr.write("Error processing %s: %s\n" % (mapcycle.location, str(e)))
            finally:
                if mfile: mfile.close()
        self.stdout.write('Successfully added "%d" maps\n' % i)
        