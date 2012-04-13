from django.utils.translation import gettext as _
from common.utils.application import is_installed
from b3portal.models import Server

PLUGINS = [('autoslap',_('Auto Slap')),
           ('chatlog',_('Chat Logger')),
           ('auditor',_('Auditor')),
           ('follow',_('Follow Players')),
           ('nickreg',_('Registered Nicks')),
           ('status',_('Status')),
           ('ipdb',_('IPDB')),
           ('ctime',_('Play Time')),
           ('map',_('Maps')),
           ('configeditor',_('Config Editor')),]

def is_plugin_installed(name):
    return is_installed('b3portal.plugins.%s' % name)

def is_plugin_enabled(server, name):
    if is_plugin_installed(name):
        if not isinstance(server, Server):
            server = Server.objects.get(uuid=server)
        mod = __import__('b3portal.plugins.%s' % name, globals(), locals(), ['is_enabled'])
        func = getattr(mod, 'is_enabled')
        return func(server)
    return False