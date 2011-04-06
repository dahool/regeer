import urllib2
import tempfile
import gzip
import os
import socket
import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

timeout = 30
socket.setdefaulttimeout(timeout)

class Command(BaseCommand):
    args = '<download_location> [(GEOIP_DAT|GEOIPCITY_DAT)]'

    def handle(self, *args, **options):
        if len(args) > 0:
            try:
                data = getattr(settings, args[1])
            except:
                data = getattr(settings, 'GEOIPCITY_DAT')
            try:
                if args[1]=='true':force = True
                elif args[1]=='false': force = False
                elif args[2]=='true': force = True
                else: force = False
            except:
                force = True
            if force:
                try:
                    self.stdout.write('Fetching %s ...\n' % args[0])
                    response = urllib2.urlopen(args[0]) 
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
                except Exception, e:
                    raise CommandError(str(e))
                self.stdout.write('Done.\n')
            else:
                self.stdout.write('Skipping.\n')
        else:
            raise CommandError("Must specify a download URL")

