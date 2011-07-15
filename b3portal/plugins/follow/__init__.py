
def is_enabled(server):
    from b3portal.plugins.follow.models import FollowPlugin
    try:
        FollowPlugin.objects.get(server=server)
    except FollowPlugin.DoesNotExist:
        return False
    return True