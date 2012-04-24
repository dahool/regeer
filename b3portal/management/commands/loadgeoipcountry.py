# -*- coding: utf-8 -*-
"""Copyright (c) 2012 Sergio Gabriel Teves
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
import urllib2
import tempfile
import gzip
import os
import socket
import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from b3portal.models import Country

timeout = 30
socket.setdefaulttimeout(timeout)

class Command(BaseCommand):
    args = '<file>'

    def handle(self, *args, **options):
        if len(args) > 0:
            filen = args[0]
        else:
            raise CommandError('Please, specify file to load.\n')

        if not os.path.exists(filen):
            raise CommandError('Cannot find the file %s.\n' % filen)
            
        try:
            data = []
            self.stdout.write('Processing file ...\n')
            f = open(filen, 'rb')
            for line in f.read().strip().splitlines():
                d = line.split(',')
                dc={'ipstart': d[0][1:-1],
                      'ipend': d[1][1:-1],
                      'ipdecstart': d[2][1:-1],
                      'ipdecend': d[3][1:-1],
                      'code': d[4][1:-1],
                      'name': d[5][1:-1]}
                data.append(dc)
            if len(data) > 0:
                self.stdout.write("Cleaning existing data ...\n")
                for m in Country.objects.all(): m.delete()
                self.stdout.write('Loading %s elements ...\n' % len(data))
                for d in data:
                    Country.objects.create(**d)
            else:
                self.stdout.write("No data was found.\n")
        except Exception, e:
            raise CommandError(str(e))
        self.stdout.write('Done.\n')
    