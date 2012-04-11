
def is_enabled(server):
    from b3portal.plugins.xlrstats.models import XlrStatsPlugin
    try:
        XlrStatsPlugin.objects.get(server=server)
    except XlrStatsPlugin.DoesNotExist:
        return False
    return True