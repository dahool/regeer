from b3portal.client.signals import add_penalty, change_penalty, delete_penalty, update_player_group
from django.dispatch import receiver

def is_enabled(server):
    from b3portal.plugins.ipdb.models import IpdbPlugin
    try:
        IpdbPlugin.objects.get(server=server)
    except IpdbPlugin.DoesNotExist:
        return False
    return True

@receiver(add_penalty, dispatch_uid="ipdb_add_penalty")
def penalty_add_callback(sender, **kwargs):
    from b3portal.plugins.ipdb.handlers import add_penalty_handler
    add_penalty_handler(kwargs['user'], kwargs['client'], kwargs['penalty'], kwargs['server'], False)

@receiver(change_penalty, dispatch_uid="ipdb_change_penalty")
def penalty_change_callback(sender, **kwargs):
    from b3portal.plugins.ipdb.handlers import add_penalty_handler
    add_penalty_handler(kwargs['user'], kwargs['client'], kwargs['penalty'], kwargs['server'], True)

@receiver(delete_penalty, dispatch_uid="ipdb_delete_penalty")
def penalty_delete_callback(sender, **kwargs):
    from b3portal.plugins.ipdb.handlers import delete_penalty_handler
    delete_penalty_handler(kwargs['user'], kwargs['client'], kwargs['penalty'], kwargs['server'])

@receiver(update_player_group, dispatch_uid="ipdb_update_player_group")
def update_player_group_callback(sender, **kwargs):
    from b3portal.plugins.ipdb.handlers import update_player_handler
    update_player_handler(kwargs['user'], kwargs['client'], kwargs['server'])
    