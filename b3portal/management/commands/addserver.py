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
import os
import getpass
import sys
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from common.utils.slug import _string_to_slug

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
        make_option('--name', dest='name', default=None,
            help='Specifies the server name.'),
        make_option('--mapcycle', dest='mapcycle', default=None,
            help='Specifies the location of the mapcycle file (ie: /home/q3ut4/mapcycle.txt)'),
        make_option('--banlist', dest='banlist', default=None,
            help=('Specifies the location of the banlist file  (ie: /home/q3ut4/banlist.txt)')),
        make_option('--statusfile', dest='statusfile', default=None,
            help=('Specifies the location of the status file (if you are using the status plugin) (ie: /home/q3ut4/status.xml)')),
        make_option('--dbname', dest='dbname', default=None,
            help=('Name of the b3 database for this server')),
        make_option('--dbuser', dest='dbuser', default=None,
            help=('Username of the b3 database for this server')),
        make_option('--dbpass', dest='dbpass', default=None,
            help=('Database password')),
        make_option('--dbhost', dest='dbhost', default=None,
            help=('Database host')),
        make_option('--rconpass', dest='rconpass', default=None,
            help=('RCON Password')),
        make_option('--plugins', dest='plugins', default=None,
            help=('List of plugins available in the server separaded by comma (chatlog,follow,flagstats,hestats,knifestats,status)')),                                                            
    )
    help = 'Used to add a server. If server already exists, edit it.'
    
    def handle(self, *args, **options):
        interactive = options.get('interactive')
        
        fields = {'name': options.get('name', None),
                  'rconpass': options.get('rconpass', None),
                  'dbname': options.get('dbname', None),
                  'dbuser': options.get('dbuser', None),
                  'dbhost': options.get('dbhost', None),
                  'dbpass': options.get('dbpass', None),
                  'mapcycle': options.get('mapcycle', None),
                  'banlist': options.get('banlist', None),
                  'statusfile': options.get('statusfile', None),
                  }
        
        plugins_s = options.get('plugins', None)
            
        databases = {}
        servers = {}

        if os.path.exists(settings.LOCAL_CONFIG):
            databases = settings.SERVER_DATABASES
            servers = settings.SERVERS
        
        if not interactive:
            for k, v in fields.items():
                if not k in ('rconpass','statusfile'):
                    raise CommandError("You must specifiy a value for --%s" % k)
            key_name = _string_to_slug(fields['name'])
        else:
            try:
                if not fields['name']:
                    fields['name'] = self.ask_input('Server name')
                key_name = _string_to_slug(fields['name'])
                if not fields['rconpass']:
                    fields['rconpass'] = self.ask_input('RCON Password (required if you want rcon management)', allow_none=True)
                if not fields['dbname']:
                    default = databases[key_name]['NAME'] if databases.has_key(key_name) else None 
                    fields['dbname'] = self.ask_input('Database name', default)
                if not fields['dbuser']:
                    default = databases[key_name]['USER'] if databases.has_key(key_name) else None
                    fields['dbuser'] = self.ask_input('Database user', default)
                if not fields['dbpass']:
                    fields['dbpass'] = self.ask_input('Database password')
                if not fields['dbhost']:
                    default = databases[key_name]['HOST'] if databases.has_key(key_name) else 'localhost'
                    fields['dbhost'] = self.ask_input('Database host', default)
                if not fields['mapcycle']:
                    default = servers[key_name]['MAPCYCLE'] if servers.has_key(key_name) else None
                    fields['mapcycle'] = self.ask_input('Location of mapcycle.txt', default)                
                if not fields['banlist']:
                    default = servers[key_name]['BANLIST'] if servers.has_key(key_name) else None
                    fields['banlist'] = self.ask_input('Location of banlist.txt', default)
                if not fields['statusfile']:
                    default = servers[key_name]['STATUS'] if servers.has_key(key_name) else None
                    fields['statusfile'] = self.ask_input('Location of status.xml (if you use status plugin)', default, allow_none=True)
                if not plugins_s == 0:
                    default = ",".join(servers[key_name]['PLUGINS']) if servers.has_key(key_name) else None
                    plugins_s = self.ask_input('List of enabled plugins separated by comma (chatlog,follow,flagstats,hestats,knifestats,status)', default, allow_none=True)
            except KeyboardInterrupt:
                sys.stderr.write("\nOperation cancelled.\n")
                sys.exit(1)

        if plugins_s:
            plugins = [s.strip() for s in plugins_s.split(',')]
        else:
            plugins = []
        
        server = {'TITLE': fields['name'],
                  'STATUS': fields['statusfile'],
                  'BANLIST': fields['banlist'],
                  'MAPCYCLE': fields['mapcycle'],
                  'RCONPASS': fields['rconpass'],
                  'PLUGINS': plugins}
        servers[key_name] = server
        db = {'NAME': fields['dbname'],
              'ENGINE': 'django.db.backends.mysql',
              'USER': fields['dbuser'],
              'PASSWORD': fields['dbpass'],
              'HOST': fields['dbhost']}
        databases[key_name] = db
        
        sys.stdout.write("\nWriting config file.\n")
        
        out = open(settings.LOCAL_CONFIG, 'w')
        out.write('SERVER_DATABASES = %s\n' % str(databases))
        out.write('SERVERS = %s\n' % str(servers))
        out.write('DATABASES.update(SERVER_DATABASES)\n')
        out.close()
        
        sys.stdout.write("\nDone.\n")
    
    def ask_input(self, text, default = None, allow_none = False):
        while 1:
            if default:
                s = " (Leave blank to use '%s')" % default
            else:
                s = ""
            value = raw_input("%s%s: " % (text,s))
            if default and value == '':
                value = default
            if value or allow_none:
                if value == '': value = None
                break
        return value