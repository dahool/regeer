
def get_server_status(server):
    from django.conf import settings
    from element import Status
    return Status(settings.SERVERS[server]['STATUS'])
    