
def is_enabled(server):
    from b3portal.plugins.ctime.models import CtimePlugin
    try:
        CtimePlugin.objects.get(server=server)
    except CtimePlugin.DoesNotExist:
        return False
    return True