from django import forms
from b3portal.rconadmin.fields import InputField, SelectField
from django.utils.translation import gettext as _
from b3portal.rconadmin.handlers import Q3ARconHandler, RconForm
from django.core import validators

class Iourt41Form(RconForm):
    
    def __init__(self, *args, **kwargs):
        maps = kwargs.pop('maps', None)
        super(Iourt41Form, self).__init__(*args, **kwargs)
        if maps:
            map_choice = [(m.name, m.display_name) for m in maps]
            self.fields['map'].choices = map_choice
            self.fields['nextmap'].choices = map_choice
        
    say = InputField(label=_('Message'), max_length=30, buttonlabel=_('Send'), required=False)
    bigtext = InputField(label=_('Big text'), max_length=20, buttonlabel=_('Send'), required=False)
    map = SelectField(label=_('Change map'), choices=(), required=False)
    nextmap = SelectField(label=_('Set next map'), choices=(), required=False)
    ban = InputField(label=_('Add IP to server ban list'), max_length=15, required=False, validators=[validators.validate_ipv4_address], error_messages={'invalid': _(u'Enter a valid IPv4 address.')})
    unban = InputField(label=_('Remove IP from server ban list'), max_length=15, required=False, validators=[validators.validate_ipv4_address], error_messages={'invalid': _(u'Enter a valid IPv4 address.')})
    password = InputField(label=_('Set server password'), max_length=10, required=False)
    write = InputField(label=_('Console'), max_length=30,  buttonlabel=_('Write'), required=False)
        
class Iourt41RconHandler(Q3ARconHandler):
    
    _commands = {'status': 'getStatus',
                 'say': 'say',
                 'bigtext': 'saybig',
                 'map': 'changeMap',
                 'nextmap': 'setNextMap',
                 'ban': 'ban',
                 'unban': 'unban',
                 'password': 'setPassword',
                 'write': 'write'}
    
    def __init__(self, server, data=None):
        self.server = server
        if data:
            self.form = Iourt41Form(data, maps=self.server.maps.all())
        else:
            self.form = Iourt41Form(maps=self.server.maps.all())
        Q3ARconHandler.__init__(self, server, data)

    def _init_console(self):
        from rconconsole.q3a.games.iourt41 import Iourt41
        self.console = Iourt41((self.server.rcon_ip, int(self.server.rcon_port)), self.server.rcon_password)
