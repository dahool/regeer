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
        