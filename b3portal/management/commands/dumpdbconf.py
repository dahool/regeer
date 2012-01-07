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
import sys
import os
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from b3portal.models import Server

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--output', dest='output', default=None,
            help='Write output to (default local.conf)'),)                                                            
    help = 'Dump server db confing to settings file'
    
    def handle(self, *args, **options):

        output = options.get('output')
        if not output: output = settings.LOCAL_CONFIG
        
        if os.path.exists(output):
             sys.stdout.write("\nRemove %s before run this command.\n" % output)
             sys.exit(1)
             
        databases = settings.DATABASES
        
        sys.stdout.write("\nReading database.\n")
        
        for server in Server.objects.all():
            db = {'NAME': str(server.database),
                  'ENGINE': str(server.engine),
                  'USER': str(server.user),
                  'PASSWORD': str(server.password),
                  'HOST': str(server.hostname)}
            databases[str(server.uuid)] = db
        
        sys.stdout.write("\nWriting config file.\n")
        
        out = open(output, 'w')
        out.write('DATABASES = %s\n' % databases)
        out.close()
        
        sys.stdout.write("\nDone.\n")