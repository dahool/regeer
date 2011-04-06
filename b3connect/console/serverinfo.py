import re

from django.conf import settings

from b3connect.console.client import B3Client
from b3connect.models import Client

color_re = re.compile(r'\^[0-9]')

class PlayerObject(object):
    
    def __init__(self, dct):
        self.name = color_re.sub('',dct['name']).strip()
        self.ip = dct['ip']
        self.ping = dct['ping']
        self.rate = dct['rate']
        self.score = dct['score']
        self.cid = dct['slot']
        
    def copy_attrs(self, dst):
        for k,v in self.__dict__.items():
            setattr(dst, k, v)
        
class ServerInfo(object):

    def __init__(self, server):
        self.currentMap = ""
        self.totalPlayers = 0
        self.updated = None
        self.currentType = ""
        self.players = []
        self.serverName = ""
        self.dbserver = server
        self.client = B3Client(settings.SERVERS[server]['CFG'])
        
    def getPlayerList(self):
        list = self.client.console.getPlayerList()
        for p in list.itervalues():
            po = PlayerObject(p)
            try:
                c = Client.objects.using(self.dbserver).get(name__exact=po.name,ip__exact=po.ip)
            except Client.DoesNotExist:
                self.players.append(po)
            except:
                raise
            else:
                po.copy_attrs(c)
                self.players.append(c)
        self.totalPlayers = len(self.players)        
        return self.players