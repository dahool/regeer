from django.conf import settings
from django.core.cache import cache
from b3portal.models import ServerBanList, Server
from gameutils import load_banlist_tupple, ip_to_decimal, ip_find_tupple
import logging

logger = logging.getLogger('regeer')

class IpBanList:
    
    def __init__(self, server):
        if isinstance(server, Server):
            self.cache_key = "banlist_%s" % server.pk
        else:
            self.cache_key = "banlist_%s" % server
        self.server = server
        self.lista = None
        
    def get_list(self):
        if not self.lista:
            self.lista = cache.get(self.cache_key)
            if self.lista is None:
                try:
                    logger.debug('Get banlist for %s' % self.server)
                    sb = ServerBanList.objects.get(server=self.server)
                except:
                    logger.debug('Banlist not found')
                    return []
                if sb.get_file():
                    self.lista = load_banlist_tupple(sb.get_file())
                else:
                    return []
                cache.set(self.cache_key, self.lista, getattr(settings, 'BANLIST_CACHE_EXPIRE', 1440) * 60)
        logger.debug('Banlist size %d' % len(self.lista))
        return self.lista

    def exists(self, ip):
        lista = self.get_list()
        elem = ip_to_decimal(ip)
        return ip_find_tupple(lista, elem) is not None