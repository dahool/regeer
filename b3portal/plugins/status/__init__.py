
def get_server_status(server):
    from b3portal.models import Server
    from b3portal.plugins.status.models import StatusPlugin
    from common.utils.file import getfile
    
    from element import Status
    
    s = Server.objects.get(uuid=server)
    sp = StatusPlugin.objects.get(server=s)
    if sp:
        return Status(getfile(sp.location))
    return None