
def is_enabled(server):
    from b3portal.plugins.map.models import MapPlugin
    try:
        MapPlugin.objects.get(server=server)
    except MapPlugin.DoesNotExist:
        return False
    return True
