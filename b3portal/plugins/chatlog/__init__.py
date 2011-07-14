
def is_enabled(server):
    from b3portal.plugins.chatlog.models import ChatLogPlugin
    try:
        ChatLogPlugin.objects.get(server=server)
    except ChatLogPlugin.DoesNotExist:
        return False
    return True