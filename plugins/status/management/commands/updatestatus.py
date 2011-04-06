from django.conf import settings
from django.core.management.base import BaseCommand
from plugins.status.element import Status
from plugins.status.models import ServerStatus, ServerStatusPlayers
from datetime import datetime

class Command(BaseCommand):
    help = 'Read status file and save summary'

    def handle(self, *args, **options):
        for server, data in settings.SERVERS.items():
            self.stdout.write("Processing %s ...\n" % server)
            try:
                status = Status(data['STATUS'])
            except Exception, e:
                self.stderr.write("Error processing %s: %s\n" % (server, str(e)))
            else:
                if status.map:
                    s = ServerStatus.objects.create(map=status.map,
                                                totalPlayers=status.totalClients,
                                                server=server,
                                                time_add=datetime.now())
                    if status.totalClients > 0:
                        for client in status.clients:
                            if client.id:
                                s.players.add(ServerStatusPlayers.objects.create(
                                                                                 server=s,
                                                                                 clientid=client.id
                                                                                 ))
            self.stdout.write("Processed %s ...\n" % server)
        self.stdout.write('Done.\n')