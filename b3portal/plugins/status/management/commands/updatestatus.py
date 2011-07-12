from django.core.management.base import BaseCommand
from b3portal.plugins.status.element import Status
from b3portal.plugins.status.models import ServerStatus, ServerStatusPlayers, StatusPlugin
from datetime import datetime
from common.utils.file import getfile

class Command(BaseCommand):
    help = 'Read status file and save summary'

    def handle(self, *args, **options):
        for conf in StatusPlugin.objects.all():
            self.stdout.write("Processing %s ...\n" % conf.server)
            try:
                status = Status(getfile(conf.location))
            except Exception, e:
                self.stderr.write("Error processing %s: %s\n" % (conf.server, str(e)))
            else:
                if status.map:
                    s = ServerStatus.objects.create(map=status.map,
                                                totalPlayers=status.totalClients,
                                                server=conf.server,
                                                time_add=datetime.now())
                    if status.totalClients > 0:
                        for client in status.clients:
                            if client.id:
                                s.players.add(ServerStatusPlayers.objects.create(
                                                                                 server=s,
                                                                                 clientid=client.id
                                                                                 ))
            self.stdout.write("Processed %s ...\n" % conf.server)
        self.stdout.write('Done.\n')