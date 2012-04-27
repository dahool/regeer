import xmlrpclib
import time
import socket

import logging

logger = logging.getLogger('regeer')

class IpdbClient:

    _EVENT_CONNECT = "connect"
    _EVENT_DISCONNECT = "disconnect"
    _EVENT_UPDATE = "update"
    _EVENT_BAN = "banned"
    _EVENT_ADDNOTE = "addnote"
    _EVENT_DELNOTE = "delnote"
    _EVENT_UNBAN = "unbanned"
    _EVENT_REFRESH = "refresh"
        
    def __init__(self, url, key, serverIpPort, timeout):
        self._key = key
        self._timeout = timeout
        self._ipPort = serverIpPort
        self._proxy = xmlrpclib.ServerProxy(url)

    def _update(self, lista):
        logging.debug(lista)
        try:
            socket.setdefaulttimeout(self._timeout)
            self._proxy.server.update(self._key, lista, int(time.time()), self._ipPort)
        except xmlrpclib.ProtocolError, protocolError:
            raise
        except xmlrpclib.Fault, applicationError:
            raise
        except socket.timeout, timeoutError:
            raise
        except socket.error, socketError:
            raise
        except Exception, e:
            raise
        finally:
            socket.setdefaulttimeout(None)
        
    def update_client(self, clientId, name, guid, ip, level, timeEdit):
        data = [self._EVENT_REFRESH, name, guid, clientId, ip, level, timeEdit]
        self._update([data])

    def add_notice(self, clientId, name, guid, ip, level, timeEdit, noticeCreated, noticeMessage, adminName, adminGuid, remoteKey):
        data = [self._EVENT_ADDNOTE, name, guid, clientId, ip, level, timeEdit, [noticeCreated, noticeMessage, adminName, adminGuid, remoteKey]]
        self._update([data])

    def del_notice(self, clientId, name, guid, ip, level, timeEdit, remoteKey):
        data = [self._EVENT_DELNOTE, name, guid, clientId, ip, level, timeEdit, [remoteKey]]
        self._update([data])
        
    def del_penalty(self, clientId, name, guid, ip, level, timeEdit):
        data = [self._EVENT_UNBAN, name, guid, clientId, ip, level, timeEdit]
        self._update([data])
    
    def add_penalty(self, clientId, name, guid, ip, level, timeEdit, penaltyCreated, penaltyDuration, penaltyReason, penaltyAdminName, penaltyAdminGuid):
        if not (penaltyDuration < 1 or penaltyDuration > 30):
            return
            
        if penaltyDuration == -1 or penaltyDuration == 0:
            pType = "pb"
        else:
            pType = "tb"

        baninfo = [pType, penaltyCreated, penaltyDuration, penaltyReason, penaltyAdminName, penaltyAdminGuid]
        data = [self._EVENT_BAN, name, guid, clientId, ip, level, timeEdit, baninfo]
        self._update([data])

    