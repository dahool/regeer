from b3portal.plugins.ipdb.ipdblib import IpdbClient
from b3portal.plugins.ipdb import ipdbsettings
from b3portal.plugins.ipdb.models import IpdbPlugin
from b3connect.models import PENALTY_TYPE_NOTICE

import logging

logger = logging.getLogger(__name__)

import time

class PluginDisabledException(Exception):
    pass

def get_client(server):
    try:
        p = IpdbPlugin.objects.get(server=server)
    except IpdbPlugin.DoesNotExist:
        raise PluginDisabledException()
    return IpdbClient(ipdbsettings.IPDB_URL, p.serverKey, ipdbsettings.IPDB_TIMEOUT)

def add_penalty_handler(user, client, penalty, server, update=False):
    
    try:
        service = get_client(server)
    except PluginDisabledException:
        return
    
    if update:
        p = None
        if client.penalties.active_bans():
            p = client.penalties.active_bans().order_by('-time_add')[0]
        if not p or p.id != penalty.id:
            logger.debug("Updated penalty is not latest")
            return

    if penalty.admin_id > 0:
        reason = penalty.reason
        admin = penalty.admin.name
        adminId = penalty.admin.guid
    else:
        reason = "%s (@%s)" % (penalty.reason, user.username)
        admin = ''
        adminId = 0     
    
    if penalty.type == PENALTY_TYPE_NOTICE:
        service.add_notice(client.id,
                        client.name,
                        client.guid,
                        client.ip,
                        client.group.level,
                        int(time.mktime(client.time_edit.timetuple())),
                        int(time.mktime(penalty.time_add.timetuple())),
                        reason,
                        admin,
                        adminId,
                        "P$%d" % penalty.id)
    else:
        service.add_penalty(client.id,
                        client.name,
                        client.guid,
                        client.ip,
                        client.group.level,
                        int(time.mktime(client.time_edit.timetuple())),
                        int(time.mktime(penalty.time_add.timetuple())),
                        penalty.duration,
                        reason,
                        admin,
                        adminId)
        
def delete_penalty_handler(user, client, penalty, server):
    
    try:
        service = get_client(server)
    except PluginDisabledException:
        return
    
    if penalty.type == PENALTY_TYPE_NOTICE:
        if penalty.data and not penalty.admin_username:
            rKey = penalty.data
        else:
            rKey = "P$%s" % penalty.id
        service.del_notice(client.id,
                        client.name,
                        client.guid,
                        client.ip,
                        client.group.level,
                        int(time.mktime(client.time_edit.timetuple())),
                        rKey)        
    else:
        if client.penalties.active_bans():
            add_penalty_handler(user, client,
                                client.penalties.active_bans().order_by('-time_add')[0],
                                server, False)
        else:
            service.del_penalty(client.id,
                        client.name,
                        client.guid,
                        client.ip,
                        client.group.level,
                        int(time.mktime(client.time_edit.timetuple())))

def update_player_handler(user, client, server):

    try:
        service = get_client(server)
    except PluginDisabledException:
        return
    
    service.update_client(client.id,
                        client.name,
                        client.guid,
                        client.ip,
                        client.group.level,
                        int(time.mktime(client.time_edit.timetuple())))
    