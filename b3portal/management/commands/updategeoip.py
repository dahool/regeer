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
import urllib2
import tempfile
import gzip
import os
import socket
import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option

timeout = 30
socket.setdefaulttimeout(timeout)

class Command(BaseCommand):

    args = '<download_location> [(GEOIP_DAT|GEOIPCITY_DAT)]'
    
    option_list = BaseCommand.option_list + (
        make_option('--no-force',
            action='store_false',
            dest='force',
            default=True,
            help='Force download if already exists'),
    )    

    def handle(self, *args, **options):
        if len(args) > 0:
            url = args[0]
            try:
                data = getattr(settings, args[1])
            except:
                data = getattr(settings, 'GEOIPCITY_DAT')            
        else:
            url = "http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz"
            data = getattr(settings, 'GEOIPCITY_DAT')

        try:
            if not os.path.exists(data) or options['force']:
                self.stdout.write('Fetching %s ...\n' % url)
                response = urllib2.urlopen(url) 
                fid, fname = tempfile.mkstemp('geo')
                out = open(fname,'wb')
                out.write(response.read())
                out.close()
                # give some time to release the file
                time.sleep(5)
                self.stdout.write('Decompressing ...\n')
                f = gzip.open(fname, 'rb')
                file_content = f.read()
                f.close()
                # delete the temp file
                self.stdout.write('Replacing %s ...\n' % data)
                dest = open(data,'wb')
                dest.write(file_content)
                dest.close()
                # give some time to release the file
                time.sleep(5)
                try:
                    os.remove(fname)
                except:
                    pass
            else:
                self.stdout.write('File %s already exists. Aborting.\n' % data)
        except Exception, e:
            raise CommandError(str(e))
        self.stdout.write('Done.\n')
