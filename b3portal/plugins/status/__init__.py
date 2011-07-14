
def is_enabled(server):
    from b3portal.plugins.status.models import StatusPlugin
    try:
        StatusPlugin.objects.get(server=server)
    except StatusPlugin.DoesNotExist:
        return False
    return True

def get_server_status(server):
    from b3portal.models import Server
    from b3portal.plugins.status.models import StatusPlugin
    from common.utils.file import getfile
    
    from element import Status
    
    s = Server.objects.get(uuid=server)
    try:
        sp = StatusPlugin.objects.get(server=s)
        if sp: return Status(getfile(sp.location))
    except:
        pass
    return None