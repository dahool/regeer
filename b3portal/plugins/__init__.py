from django.utils.translation import gettext as _
from common.utils.application import is_installed
from b3portal.models import Server

PLUGINS = [('autoslap',_('Auto Slap')),
           ('chatlog',_('Chat Logger')),
           ('follow',_('Follow Players')),
           ('nickreg',_('Registered Nicks')),
           ('status',_('Status')),
           ('ipdb',_('IPDB')),
           ('map',_('Maps'))]

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