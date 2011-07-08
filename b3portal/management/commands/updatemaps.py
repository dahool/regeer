from django.core.management.base import BaseCommand
from b3portal.models import Map
from django.conf import settings

class Command(BaseCommand):
    help = 'Fill maps table'

    def handle(self, *args, **options):

        self.stdout.write("Cleaning existing data...\n")
        for m in Map.objects.all():
            m.delete()

        i=0
        for key, server in settings.SERVERS.items():
            if server.has_key('MAPCYCLE'):
                mfile = open(server['MAPCYCLE'])
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
                                Map.objects.create(name=m, server=key)
                                i+=1
            
        self.stdout.write('Successfully added "%d" maps\n' % i)
