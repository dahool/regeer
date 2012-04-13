
def is_enabled(server):
    from b3portal.plugins.configeditor.models import ConfigEditorPlugin
    try:
        ConfigEditorPlugin.objects.get(server=server)
    except ConfigEditorPlugin.DoesNotExist:
        return False
    return True