from django import forms
from b3portal.rconadmin.fields import InputField, SelectField
from django.utils.translation import gettext as _

class Iourt41Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        maps = kwargs.pop('maps', None)
        super(Iourt41Form, self).__init__(*args, **kwargs)
        if maps:
            map_choice = [(m.name, m.display_name) for m in maps]
            self.fields['map'].choices = map_choice
            self.fields['nextmap'].choices = map_choice
        
    say = InputField(label=_('Message'), max_length=30, buttonlabel=_('Send'))
    saybig = InputField(label=_('Big text'), max_length=20, buttonlabel=_('Send'))
    map = SelectField(label=_('Change map'), choices=())
    nextmap = SelectField(label=_('Set next map'), choices=())
    ban = InputField(label=_('Add IP to server ban list'), max_length=15)
    unban = InputField(label=_('Remove IP from server ban list'), max_length=15)
    password = InputField(label=_('Set server password'), max_length=10)
    write = InputField(label=_('Console'), max_length=30)
    
class Iourt41RconHandler:
    
    def __init__(self, server, data=None):
        if data:
            self.form = Iourt41Form(data, maps=server.maps.all())
        else:
            self.form = Iourt41Form(maps=server.maps.all())
