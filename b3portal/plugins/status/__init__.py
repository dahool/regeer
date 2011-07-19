
def is_enabled(server):
    from b3portal.plugins.status.models import StatusPlugin
    try:
        StatusPlugin.objects.get(server=server)
    except StatusPlugin.DoesNotExist:
        return False
    return True