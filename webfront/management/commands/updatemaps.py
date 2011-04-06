from django.core.management.base import BaseCommand
from webfront.models import Map

class Command(BaseCommand):
    args = '<mapcycle.txt mapcycle.txt ...>'
    help = 'Fill maps table'

    def handle(self, *args, **options):
        list = set()
        for mp in args:
            mfile = open(mp)
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
                            list.add(m)
        
        self.stdout.write("Cleaning existing data...\n")
        for m in Map.objects.all():
            m.delete()

        for m in list:
            Map.objects.create(name=m)
            
        self.stdout.write('Successfully added "%d" maps\n' % len(list))
