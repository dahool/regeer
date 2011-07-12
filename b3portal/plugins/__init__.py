from django.utils.translation import gettext as _
from common.utils.application import is_installed

PLUGINS = [('autoslap',_('AutoSlap Plugin')),
           ('chatlog',_('ChatLogger Plugin')),
           ('follow',_('Follow Players Plugin')),
           ('nickreg',_('Registered Nicks Plugin')),
           ('status',_('Status Plugin')),]

def is_plugin_installed(name):
    return is_installed('b3portal.plugins.%s' % name)
