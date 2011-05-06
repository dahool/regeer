import os
import getpass
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from common.utils.slug import _string_to_slug

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--name', dest='name', default=None,
            help='Specifies the server name.'),
        make_option('--mapcycle', dest='mapcycle', default=None,
            help='Specifies the location of the mapcycle file (ie: /home/q3ut4/mapcycle.txt)'),
        make_option('--banlist', dest='banlist', default=None,
            help=('Specifies the location of the banlist file  (ie: /home/q3ut4/banlist.txt)')),
        make_option('--statusfile', dest='statusfile', default=None,
            help=('Specifies the location of the status file (if you are using the status plugin) (ie: /home/q3ut4/status.xml)')),
        make_option('--dbname', dest='dbname', default='b3',
            help=('Name of the b3 database for this server')),
        make_option('--dbuser', dest='dbuser', default='b3',
            help=('Username of the b3 database for this server')),
        make_option('--dbpass', dest='dbpass', default=None,
            help=('Database password')),
        make_option('--dbhost', dest='dbhost', default='localhost',
            help=('Database host')),
        make_option('--rconpass', dest='rconpass', default=None,
            help=('RCON Password')),
        make_option('--plugins', dest='plugins', default=None,
            help=('List of plugins available in the server separaded by comma (chatlog,follow,flagstats,hestats,knifestats,status)')),                                                            
    )
    help = 'Used to add a server'
    
    def handle(self, *args, **options):
        name = options.get('name', None)
        mapcycle = options.get('mapcycle', None)
        banlist = options.get('banlist', None)
        statusfile = options.get('statusfile', None)
        dbname = options.get('dbname', None)
        dbuser = options.get('dbuser', None)
        dbhost = options.get('dbhost', None)
        dbpass = options.get('dbpass', None)
        rconpass = options.get('rconpass', None)
        plugins_s = options.get('plugins', None)
        if plugins_s:
            plugins = [s.strip() for s in plugins_s.split(',')]
        else:
            plugins = []
            
        databases = {}
        servers = {}
        
        if os.path.exists(settings.LOCAL_CONFIG):
            databases = settings.SERVER_DATABASES
            servers = settings.SERVERS
        
        slug_name = _string_to_slug(name)
        server = {'TITLE': name,
                  'STATUS': statusfile,
                  'BANLIST': banlist,
                  'MAPCYCLE': mapcycle,
                  'RCONPASS': rconpass,
                  'PLUGINS': plugins}
        servers[slug_name] = server
        db = {'NAME': dbname,
              'ENGINE': 'django.db.backends.mysql',
              'USER': dbuser,
              'PASSWORD': dbpass,
              'HOST': dbhost}
        databases[slug_name] = db
        
        out = open(settings.LOCAL_CONFIG, 'w')
        out.write('SERVER_DATABASES = %s\n' % str(databases))
        out.write('SERVERS = %s\n' % str(servers))
        out.write('DATABASES.update(SERVER_DATABASES)\n')
        out.close()
    
