from django import forms
from b3portal.rconadmin.fields import InputField, SelectField
from django.utils.translation import gettext as _

MAP = (
    ('m', _('MAP1')),
    ('h', _('MAP2')),
)

class Iourt41Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        maps = kwargs.pop('maps', None)
        super(Iourt41Form, self).__init__(*args, **kwargs)
        if maps:
            map_choice = [(m.display_name, m.name) for m in maps]
            self.fields['map'].choices = map_choice
            self.fields['nextmap'].choices = map_choice
        
    say = InputField(label=_('Message'), max_length=15)
    saybig = InputField(label=_('Big text'), max_length=15)
    map = SelectField(label=_('Change map'), choices=())
    nextmap = SelectField(label=_('Set next map'), choices=())
    ban = InputField(label=_('Add IP to server ban list'), max_length=15)
    unban = InputField(label=_('Remove IP from server ban list'), max_length=15)
    password = InputField(label=_('Set server password'), max_length=10)
    
class Iourt41RconHandler:
    
    def __init__(self, server):
        self.form = Iourt41Form(maps=server.maps.all())
